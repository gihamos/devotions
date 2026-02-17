import os
from dotenv import load_dotenv
from utils.logger import logger
from pymongo import MongoClient

load_dotenv()
_MONGODBURL=os.getenv("MONGODBURL");

if(_MONGODBURL is None):
    logger.error("la variable d'environement << MONGODBURL >> est manquante ")
    exit(-1)


def initdb():
    try:
        client = MongoClient(_MONGODBURL)
        db = client.devotions_db
        return db
    except Exception as e:
        logger.error(f"erreur lors de l'accès à la base de donnée \n message: {e} \n")
        



