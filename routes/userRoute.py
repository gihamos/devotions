from fastapi import APIRouter, Body, Response, Depends,HTTPException
from data.database import user_collection
from data.model.model import UserModel
from dependencies.authDependency import userAuth_dependency
from dependencies.roleDependency import userAdminRole_dependency
from utils.security import get_password_hash
from pymongo.errors import DuplicateKeyError

_router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(userAuth_dependency),Depends(userAdminRole_dependency)]
    
)

@_router.post("/create")
async def create_user(data: UserModel):
    doc = data.model_dump()
    doc["hashed_password"]=get_password_hash(doc.pop("password"))
    try:
        # comment: 
         result = user_collection.insert_one(doc)
         return {"id": str(result.inserted_id)}
    except DuplicateKeyError:
        raise HTTPException(status_code=406,detail="cet adresse mail ou ce username existe déjà")
    # end try
   
   
