from pydantic import BaseModel, Field,EmailStr
from enum import Enum
from typing import List, Optional, Any
from datetime import datetime

class Role(str,Enum):
    """
    user role: 
    """
    ADMIN = "admin"
    READ = "read_only"


class BookNode(BaseModel):
    id: Optional[str]
    parentId: Optional[str] = None

    type: str  # "book", "chapter", "section", "paragraph"
    level: int
    order: int  # position dans le parent

    title: Optional[str] = None

    # Contenu
    original: Optional[str] = None      # texte brut
    clean: Optional[str] = None         # texte nettoyé
    formatted: Optional[str] = None     # markdown / html

    # Enrichissements IA
    summary: Optional[str] = None
    keywords: Optional[List[str]] = []
    entities: Optional[List[dict]] = []     # ex: [{"type": "person", "text": "Yann"}]
    sentiment: Optional[float] = None       # -1 = négatif, 0 = neutre, +1 = positif
    embedding: Optional[List[float]] = []   # vecteur pour recherche sémantique

    # Infos utiles
    wordCount: Optional[int] = None
    path: Optional[str] = None

    meta: dict = {}
    references: List[Any] = []

    children: List["BookNode"] = []

    class Config:
        from_attributes = True
        populate_by_name = True

BookNode.model_rebuild()

class Book(BaseModel):
    id: Optional[str] = Field(alias="_id")

    title: Optional[str]
    description: Optional[str]
    language: str = "fr"

    releaseDate: Optional[datetime]
    publicationDate: Optional[datetime]
    startedAt: Optional[datetime]

    summary: Optional[str] = None
    keywords: Optional[List[str]] = []
    entities: Optional[List[dict]] = []
    sentiment: Optional[float] = None
    embedding: Optional[List[float]] = []
    wordCount: Optional[int] = None

    children: List[BookNode] = []

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


