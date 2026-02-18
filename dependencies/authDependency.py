from fastapi import HTTPException, Request
import jwt
from params import ALGORITHM, JWT_SECRET

async def auth_dependency(request: Request):
    auth_header = request.headers.get("Authorization")

    # Vérification du header Authorization
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Token manquant ou invalide")

    token = auth_header.split(" ")[1]

    try:
        # Décodage du JWT
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        request.state.user = payload

        # Vérification du device_id
        device_id_cookie = request.cookies.get("device_id")
        token_device_id = payload.get("device_id")

        if not device_id_cookie or not token_device_id or device_id_cookie != token_device_id:
            raise HTTPException(401, "Appareil non reconnu")

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expiré")

    except jwt.InvalidTokenError:
        raise HTTPException(401, "Token invalide")

    return payload  
