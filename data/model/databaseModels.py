from pydantic import BaseModel, Field,EmailStr
from enum import Enum

class Role(str,Enum):
    """
    user role: 
    """
    ADMIN = "admin"
    READ = "read_only"

from typing import List, Optional, Any
from datetime import datetime

class TextFragment(BaseModel):
    id: Optional[str]
    text: Optional[str]
    format: Optional[List[str]] = []

class RichText(BaseModel):
    fragments: List[TextFragment] = []


class Line(BaseModel):
    id: Optional[str]
    richText: Optional[RichText]

class BookNode(BaseModel):
    id: Optional[str]
    type: Optional[str]            
    level: Optional[int] = None

    title: Optional[str] = None

    lines: Optional[List[Line]] = []
    formattedContent: Optional[str] = None
    originalContent: Optional[str] = None
    content: Optional[str] = None

    meta: Optional[dict] = {}
    references: Optional[List[Any]] = []

    children: Optional[List["BookNode"]] = []
    
    class Config: 
        from_attributes = True
        populate_by_name = True
    
BookNode.model_rebuild()
    

class Book(BaseModel):
    id: Optional[str] = Field(alias="_id")

    title: Optional[str]
    description: Optional[str]
    language:Optional[str]="fr"
    releaseDate: Optional[datetime]
    publicationDate: Optional[datetime]
    startedAt: Optional[datetime]

    #prompt: Optional[str] = None

    children: Optional[List[BookNode]] = []
    
    class Config: 
        from_attributes = True
        populate_by_name = True
    
class User(BaseModel):
    id: Optional[str] = Field(alias="_id")
    username:str
    email:Optional[EmailStr]=None
    hashed_password:Optional[str]=None
    first_name:Optional[str]
    last_name:Optional[str]
    role:Role=Role.READ
    
    class Config: 
        from_attributes = True
        populate_by_name = True


