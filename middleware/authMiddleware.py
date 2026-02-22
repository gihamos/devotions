from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from fastapi import HTTPException, Request
from starlette.types import ASGIApp, Receive, Scope, Send
from params import ALGORITHM,JWT_SECRET
import jwt

class AuthMiddlawre(BaseHTTPMiddleware):
     async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
          auth_header = request.headers.get("Authorization")
          if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                playload=jwt.decode(token,JWT_SECRET,[ALGORITHM])
                request.state.user=playload
                device_id_cookie = request.cookies.get("device_id")
                token_device_id = playload.get("device_id")
                
                if not device_id_cookie or not token_device_id or device_id_cookie != token_device_id: 
                    raise HTTPException(401, "Appareil non reconnu")
                
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expiré")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Token invalide")
            
            else:
                request.state.user = None
                
            
           
            return await call_next(request)
