from pydantic import BaseModel,EmailStr
from typing import Optional
from data.model.databaseModels import Role

class UserLoginModel(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    login:str
    password:str
    
class UserModel(BaseModel):
    username:str
    email:EmailStr
    password:str
    first_name:Optional[str]
    last_name:Optional[str]
    role:Role=Role.READ
    
    
