from fastapi import HTTPException, Request,Depends
import jwt
from params import ALGORITHM, JWT_SECRET
from fastapi.security import HTTPBearer
bearer_scheme = HTTPBearer()

async def userAuth_dependency( request: Request, credentials = Depends(bearer_scheme)):



    try:
        # Décodage du JWT
        token=credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        request.state.user = payload

        # Vérification du device_id
        device_id_cookie = request.cookies.get("device_id")
        token_device_id = payload.get("device_id")

        if not device_id_cookie or not token_device_id or device_id_cookie != token_device_id:
            raise HTTPException(401, "Appareil non reconnu")
        
        if not payload.get("type") and payload.get("type")!="user":
             raise HTTPException(401, "access non autorisé")

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expiré")

    except jwt.InvalidTokenError:
        raise HTTPException(401, "Token invalide")

    return payload  
