from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import  Request
from utils.logger import logger

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        logger.info(f"{request.method} {request.url}   {response.status_code}")
        return response
