from fastapi import FastAPI
from routers import users, jwt_auth_users
from fastapi.staticfiles import StaticFiles

#Montar server con el comando uvicorn main:app --reload
#LocalHost : http://127.0.0.1:8000
#Documentacion: http://127.0.0.1:8000/doc
#Documentacion: http://127.0.0.1:8000/redoc

app = FastAPI()

app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name = "static")

@app.get("/") 
async def root():
    return {"message": "Hola FastAPI"}
