import yt_dlp
import os
import whisper
from params import BASE_DIR,Path

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
