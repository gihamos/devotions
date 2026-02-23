from fastapi import HTTPException, Request
from data.model.databaseModels import Role
import jwt

async def userRole_dependency(request: Request, role: Role):
    if not getattr(request.state, 'user', None):
        raise HTTPException(status_code=401, detail="utilisateur non authentifié")
    print("\ndata request: ",request.state.user,"\n")
    user_data = request.state.user
    
    if "role" not in user_data: 
        raise HTTPException(status_code=400, detail="Rôle manquant dans le token")

    local_role = Role(user_data["role"])

    if local_role != role:
        raise HTTPException(status_code=403, detail="vous n'avez pas les droits")
    
async def userAdminRole_dependency(request: Request):
    if not getattr(request.state, 'user', None):
        raise HTTPException(status_code=401, detail="utilisateur non authentifié")
    
    user_data = request.state.user
 
    if "role" not in user_data: 
     raise HTTPException(status_code=400, detail="Rôle manquant dans le token")


    local_role = Role(user_data["role"])


    if local_role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")