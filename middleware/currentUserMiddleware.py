from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from data.database import user_collection

class CurrentUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_payload = getattr(request.state, "user", None)

        if user_payload:
            user = user_collection.find_one({"_id": user_payload["id"]})
            request.state.current_user = user
        else:
            request.state.current_user = None

        return await call_next(request)
