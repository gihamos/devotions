import yt_dlp
import os
import tempfile
import whisper
import json
import pdfplumber
import re
from docx import Document
from odf.opendocument import load
from odf.text import P
from params import BASE_DIR,Path
from moviepy.video.io.VideoFileClip import VideoFileClip 

def preview_edges(text: str, start_len: int = 25, end_len: int = 20) -> str:
    """cette methode permet de tronquer le texte

    Args:
        text (str): _description_
        start_len (int, optional): _description_. Defaults to 25.
        end_len (int, optional): _description_. Defaults to 20.

    Returns:
        str: _description_
    """
    if not text:
        return ""

    if len(text) <= start_len + end_len:
        return text

    return text[:start_len] + "..." + text[-end_len:]


def download_youtube_audio(url: str, output_dir: str = BASE_DIR / "downloads") -> str:
    """
    Télécharge l'audio d'une vidéo YouTube et retourne le chemin du fichier audio.
    """

    # Créer le dossier si nécessaire
    dw_path=Path(output_dir)
    dw_path.mkdir(exist_ok=True)

    # Chemin final du fichier audio
    output_path = os.path.join(output_dir, "audio.%(ext)s")
    
    ydl_opts = {
    "format": "bestaudio[ext=m4a]/bestaudio/best",
    "outtmpl": os.path.join(output_dir, "audio.%(ext)s"),
    "quiet": True
}



    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
         ydl.download([url])

    
    for file in os.listdir(output_dir):
        if file.startswith("audio."):
            return os.path.join(output_dir, file)

    raise FileNotFoundError("Impossible de trouver le fichier audio téléchargé.")

def transcript(audio_path:str):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

def transcript_with_timestamps(audio_path: str): 
    model = whisper.load_model("base") # ou "small", "medium" 
    result = model.transcribe(audio_path) 
    segments = [] 
    part=result["segments"]
    for seg in part: 
        segments.append({ "start": seg["start"], 
                         "end": seg["end"], 
                         "text": seg["text"] }) 
    return segments


def extract_audio_from_video(video_path, output="downloads/audio.mp3"):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output)
    return output




async def extract_text_from_file(file):
    content = await file.read()
    mime = file.content_type

    # -----------------------------
    # 1) TEXT / CSV
    # -----------------------------
    if mime.startswith("text/"):
        return content.decode("utf-8", errors="ignore")

    # -----------------------------
    # 2) JSON
    # -----------------------------
    elif mime == "application/json":
        data = json.loads(content.decode("utf-8", errors="ignore"))
        return json.dumps(data, indent=2, ensure_ascii=False)

    # -----------------------------
    # 3) PDF
    # -----------------------------
    elif mime == "application/pdf":
        text = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    # -----------------------------
    # 4) DOCX
    # -----------------------------
    elif mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file.file)
        return "\n".join([p.text for p in doc.paragraphs])

    # -----------------------------
    # 5) ODT (LibreOffice)
    # -----------------------------
    elif mime == "application/vnd.oasis.opendocument.text":
        doc = load(file.file)
        paragraphs = doc.getElementsByType(P)
        return "\n".join([p.firstChild.data if p.firstChild else "" for p in paragraphs])

    # -----------------------------
    # 6) AUDIO (mp3, wav, m4a…)
    # -----------------------------
    elif mime.startswith("audio/"):
        # Sauvegarde temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".audio") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        model = whisper.load_model("base")
        result = model.transcribe(tmp_path)

        os.remove(tmp_path)
        return result["text"]

    # -----------------------------
    # 7) VIDEO (mp4, avi, mov…)
    # -----------------------------
    elif mime.startswith("video/"):
        # Sauvegarde temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".video") as tmp:
            tmp.write(content)
            video_path = tmp.name

        # Extraire l’audio
        audio_path = video_path + ".mp3"
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)

        # Transcrire
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)

        # Nettoyage
        clip.close()
        os.remove(video_path)
        os.remove(audio_path)

        return result["text"]
    


    else :
        raise ValueError("Format non supporté")



def remove_think_blocks(text: str) -> str:
    """
    Supprime les blocs <think>...</think> renvoyés par certains modèles.
    """
    if not text:
        return text

    # Supprime tout bloc <think>...</think>
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Nettoyage final
    return cleaned.strip()


def strip_markdown_json(text: str) -> str:
    if not isinstance(text, str):
        return text

    cleaned = re.sub(r"```json(.*?)```", r"\1", text, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"```(.*?)```", r"\1", cleaned, flags=re.DOTALL)
    return cleaned.strip()


def safe_parse(text):
    # Cas 1 : déjà un dict → rien à faire
    if isinstance(text, dict):
        return text

    # Cas 2 : None ou vide
    if text is None:
        return None

    # Cas 3 : string → parse JSON
    if isinstance(text, str):
        try:
            cleaned = strip_markdown_json(text)
            return json.loads(cleaned)
        except Exception:
            return None

    
    return None


def chunk_text(text: str, max_size: int = 5000):
    """
    Découpe le texte en chunks sans couper les mots.
    """
    words = text.split()
    current_chunk = []

    current_length = 0
    for word in words:
        # +1 pour l'espace ajouté entre les mots
        if current_length + len(word) + 1 > max_size:
            yield " ".join(current_chunk)
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1

    if current_chunk:
        yield " ".join(current_chunk)


def smart_chunk_text(text: str, max_size: int = 5000):
    """
    Découpe le texte en chunks intelligents :
    - d'abord par paragraphes
    - puis par phrases
    - puis par mots
    Sans jamais couper un mot.
    """
    paragraphs = text.split("\n\n")
    current = ""

    for para in paragraphs:
        if len(current) + len(para) < max_size:
            current += para + "\n\n"
        else:
            # si le paragraphe est trop long, découper en phrases
            sentences = re.split(r'(?<=[.!?]) +', para)
            for sent in sentences:
                if len(current) + len(sent) < max_size:
                    current += sent + " "
                else:
                    yield current.strip()
                    current = sent + " "

    if current.strip():
        yield current.strip()


def getJsonLLmMessage(msg_system:str,msg_user,text:str)->list[list[dict[str,any]]]:
    chunks=list(smart_chunk_text(text,5000))
    
    messages=[
       
    ]
    for idx, chunk in enumerate(chunks):
        message = f""" 
                         {msg_user}
                         
                    ======== Voici le texte à traiter ==== 
                            {chunk} 
                    =======================================
                    """
        messages.append([
             {"role": "system",
              "content": msg_system},
            {
            "role":"user",
            "content":message
        }])
     
    
    return messages