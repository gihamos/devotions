import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent

MONGODBURL=os.getenv("MONGODBURL")
JWT_SECRET=os.getenv("JWT_SECRET","728277004765f2f6e7d9b3d26e9c722f")