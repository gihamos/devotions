from fastapi import APIRouter, Body, Response, Depends, HTTPException, File, UploadFile
from data.database import user_collection
from data.model.model import UserModel
from dependencies.authDependency import userAuth_dependency
from dependencies.roleDependency import userAdminRole_dependency
from utils.security import get_password_hash
from pymongo.errors import DuplicateKeyError
from utils.fonction import extract_text_from_file
from ai.agents import ExtractorBookAgent
from ai.services import universalLLMService

_router = APIRouter(
    prefix="/agent",
    tags=["agent", "ai"],
    dependencies=[Depends(userAuth_dependency)]
    
)



from fastapi import UploadFile, File, HTTPException

ALLOWED_MIME_TYPES = {
    # Text
    "text/plain",
    "text/csv",
    "application/json",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.oasis.opendocument.text",

}

@_router.post("/extractBook",dependencies=[Depends(userAdminRole_dependency)])
async def extractBook(file: UploadFile = File(...)):
    
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=403,
            detail=f"Format non supporté : {file.content_type}"
        )

    text = await extract_text_from_file(file)

    
    llm=universalLLMService.UniversalLLMService()
    agent=ExtractorBookAgent.ExtractorBookAgent(llm=llm)
    data=await agent.run({"text":text})

    return {
        "filename": file.filename,
        "mime": file.content_type,
        "text": data
    }







