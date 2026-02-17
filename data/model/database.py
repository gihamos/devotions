
from params import MONGODBURL
from utils.logger import logger
from pymongo import MongoClient


if(MONGODBURL is None):
    logger.error("la variable d'environement << MONGODBURL >> est manquante ")
    exit(-1)


def initdb():
    try:
        client = MongoClient(MONGODBURL)
        db = client.devotions_db
        return db
    except Exception as e:
        logger.error(f"erreur lors de l'accès à la base de donnée \n message: {e} \n")
        
_db = initdb()

book_collection = _db.books
user_collection=_db.users
user_collection.create_index("username",unique=True)
user_collection.create_index("email",unique=True)




