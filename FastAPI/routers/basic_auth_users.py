from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#OAuth2PasswordBearer gestiona la autenticacion
#OAuth2PasswordRequestForm forma en la que se envian los datos al backend para autenticarlo

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username : str
    full_name : str
    email : str
    disabled : bool
    
class User_DB(User):
    password : str

users_db = {
    "aeizaguerri":{
        "username" : "User1",
        "full_name" : "User1_Name User1_Surname",
        "email" : "User1@mail.com",
        "disabled" : False,
        "password" : "123456"
    },
    "anizhm":{
        "username" : "User2",
        "full_name" : "User2_Name User2_Surname",
        "email" : "User2@mail.com",
        "disabled" : True,
        "password" : "654321"
    }
}

#Busca un usuario en la BD y retorna un usuario de la clase Users
def search_user(username : str):
    if username in users_db:
        return User(**users_db[username])

#Busca un usuario en la BD y retorna un usuario de la clase Users_db que incluye la contraseña   
def search_user_db(username : str):
    if username in users_db:
        return User_DB(**users_db[username])

#Comprueba que el usuario este pasando el token correcto
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,
                            detail="Credenciales invalidas",
                            headers={"WWW-Authenticate" : "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,
                            detail="Usuario inactivo")
        
    return user

#Se le pasa un formulario con usuario y contraseña y comprueba en la bd si existe el usuario
#y en caso de que exista se comprueba su contraseña. Si ambos son correctos, la API responde con 
#un token de autenticacion

@app.post("/login")
async def login(form : OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail= "Usuario incorrecto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail= "Contraseña incorrecta")
        
    return {"access_token":user.username, "token_type":"bearer"}

#Esta funcion solo funciona si se le pasa el token, lo que significa que para acceder
#se debe estar autenticado

@app.get("/users/profile")
async def profile(user: User = Depends(current_user)):
    return user
