import yt_dlp
import os
from params import BASE_DIR

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


def download_youtube_audio(url: str, output_dir: str = f"{BASE_DIR}/downloads") -> str:
    """
    Télécharge l'audio d'une vidéo YouTube et retourne le chemin du fichier audio.
    """

    # Créer le dossier si nécessaire
    os.makedirs(output_dir, exist_ok=True)

    # Chemin final du fichier audio
    output_path = os.path.join(output_dir, "audio.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Trouver le fichier téléchargé (m4a, webm, etc.)
    for file in os.listdir(output_dir):
        if file.startswith("audio."):
            return os.path.join(output_dir, file)

    raise FileNotFoundError("Impossible de trouver le fichier audio téléchargé.")

