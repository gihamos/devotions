from fastapi import APIRouter,HTTPException,Body,Request,Response
from data.model.model import UserLoginModel
from data.database import user_collection
from data.model.convertData import to_user_model
from utils.security import verify_password,create_access_token
from uuid import uuid4
_router=APIRouter(prefix="/auth")

@_router.post(path="/login")
async def login(response :Response,request:Request, data: UserLoginModel= Body(...)):
    user=user_collection.find_one(filter={
       "$or": [ {"username": {"$regex": f"^{data.login}$", "$options": "i"}}, 
               {"email": {"$regex": f"^{data.login}$", "$options": "i"}} ]
       })
    if user is None:
        raise HTTPException(status_code=401, detail="utilisateur ou mot de passe incorrect")
    user_model=to_user_model(user)
    if not verify_password(data.password, str(user_model.hashed_password)):
        raise HTTPException(status_code=401, detail="Identifiants invalides") 
    device_id = request.cookies.get("device_id") or str(uuid4())
    token = create_access_token({
                                   "user_id": user_model.id,
                                   "device_id": device_id,
                                   "username":user_model.username,
                                    "email":user_model.email
                                  }) 
    
    playload={
        "access_token":token,
        "token_type": "bearer",
        "user":{
            "username":user_model.username,
            "email":user_model.email,
            "first_name":user_model.first_name,
            "last_name":user_model.last_name
        }
    }
    
    response.set_cookie( "device_id", device_id,
                        max_age=3600 * 24 * 365,
                        httponly=True, 
                        secure=False,
                        samesite="lax" )
    return playload