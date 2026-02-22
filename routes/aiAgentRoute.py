from fastapi import APIRouter, Body, Response, Depends, HTTPException, File, UploadFile
from data.database import user_collection
from data.model.model import UserModel
from dependencies.authDependency import userAuth_dependency
from dependencies.roleDependency import userAdminRole_dependency
from utils.security import get_password_hash
from pymongo.errors import DuplicateKeyError

_router = APIRouter(
    prefix="/agent",
    tags=["agent", "ai"],
    dependencies=[Depends(userAuth_dependency)]
)

@_router.post("/createBook")
async def insertBook(file: UploadFile = File(...)):
    # Vérifier que le fichier est bien fourni
    if file is None:
        raise HTTPException(status_code=400, detail="Aucun fichier reçu")

    if not file.content_type.startswith("application/") and not file.content_type.startswith("text/"):
        raise HTTPException(status_code=400, detail="Format de fichier non supporté")

    content = await file.read()

    


    return {
            "status_code":200,
            "detail": "Livre reçu avec succès", 
            "filename": file.filename
            }
