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
