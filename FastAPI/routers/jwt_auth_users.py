from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 
SECRET = "0680bc1ec7fa13ae68e53ff29d4c83307e4458aa158ea2e26dc183f2f420aec9"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username : str
    full_name : str
    email : str
    disabled : bool
    
class User_DB(User):
    password : str

users_db = {
    "aeizaguerri":{
        "username" : "aeizaguerri",
        "full_name" : "Alberto Eizaguerri",
        "email" : "aeiza@ggg.com",
        "disabled" : False,
        "password" : "$2a$12$UBxLjQQoQxSNFqgdmp9N7eoyXfiNYSmU0e7os5RoHPLjoVkVsT2iW"
    },
    "anizhm":{
        "username" : "anizhm",
        "full_name" : "Anai Hernandez",
        "email" : "abogada@ggg.com",
        "disabled" : True,
        "password" : "$2a$12$fVlWf7rp1KQXfOM6AD7npu4Es6SfrnbHWIm5NQmTFvw5BqsRCyi4a"
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


async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,
                            detail="Credenciales invalidas",
                            headers={"WWW-Authenticate" : "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        
        if  username is None:
            raise exception
        
        return search_user(username)
            
    except JWTError:
        raise exception
    
    

async def current_user(user: User = Depends(auth_user)):
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,
                            detail="Usuario inactivo")
        
    return user


@router.post("/login")
async def login(form : OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail= "Usuario incorrecto")
    
    user = search_user_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail= "Contraseña incorrecta")
    
    access_token = {"sub":user.username,
                    "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token":jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type":"bearer"}


@router.get("/users/profile")
async def profile(user: User = Depends(current_user)):
    return user