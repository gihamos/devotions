import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent

MONGODBURL=os.getenv("MONGODBURL")
JWT_SECRET=os.getenv("JWT_SECRET", default="12c772d5f202e6e965733a956e0a32f5c12c3d500452844cb63d50c1aa478090")
ALGORITHM = "HS256"
FFMPEG_PATH=BASE_DIR / "module/windows/ffmpeg/bin"

os.environ["PATH"] += os.pathsep + os.path.abspath(FFMPEG_PATH)