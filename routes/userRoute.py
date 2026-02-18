from fastapi import APIRouter, Body, Response, Depends
from data.database import user_collection
from data.model.model import UserModel
from dependencies.authDependency import auth_dependency
from utils.security import get_password_hash

_router = APIRouter(
    prefix="/user",
    tags=["user"],
    
)

@_router.post("/create")
async def create_user(data: UserModel):
    doc = data.model_dump()
    doc["hashed_password"]=get_password_hash(doc.pop("password"))
    result = user_collection.insert_one(doc)
    return {"id": str(result.inserted_id)}
