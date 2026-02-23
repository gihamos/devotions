from fastapi import FastAPI
from middleware.loggerMiddleware import LoggerMiddleware

from utils.logger import logger
from routes import authentificateRoute,userRoute,aiAgentRoute

app=FastAPI(title="ceci est l'api permettant d'accéder à des devotion",
            version="1.0",
            contact={
                "name":"Taise de these NGANGA YABIE",
                "email":"gihamos@gmail.com"
            })


app.add_middleware(LoggerMiddleware)

app.include_router(authentificateRoute._router)
app.include_router(userRoute._router)
app.include_router(aiAgentRoute._router)

logger.info(msg="Demarage de l'application")
@app.get("/")
def home():
    return {
        "message": "api fonctionnel"
    } 
    