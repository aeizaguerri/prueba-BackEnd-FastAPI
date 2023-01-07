from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

#lanza el servidor utilizando el comando uvicorn users:app -- reload (acuerdate de guardar antes para que funcione)
router = APIRouter(prefix = "/user", 
                tags=["users"],
                responses= {404 : {"message" : "No encontrado"}})

#Creando una entidad utlizando BaseModel, se interpreta conmo un JSON por FastAPI
class User(BaseModel):
    id : int
    name : str
    surname : str
    url : str
    age : int

users_list = [
    User(id = 1, name = "Alberto", surname = "Eiza",url =  "aeiza.com",age = 24),
    User(id = 2, name = "Juan", surname = "Eiza",url =  "jeiza.com",age = 20),
    User(id = 3, name = "Aniz", surname = "Hernandez",url =  "abogada.com",age = 25)
    ]

#Busqueda de usuarios en la db fake y manejo de errores
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario con el id"}

#Saca toda la lista de usuarios de una supuesta db fake
@router.get("/")
async def users():
    return users_list

#Saca solo el usuario que se le indique en la url
@router.get("/{id}")
async def user(id : int):
    return search_user(id)

#Saca el usuario utilizando query
#Poniendo ./?{parametro}=x en la url pasas el valor x directamente a la funcion
@router.get("/")
async def user(id : int):
    return search_user(id)

#Post inserta valores
@router.post("/", status_code=201)
async def user(user : User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    
    users_list.append(user)
    return user
        
#Put actualiza varios, pero sepuede usar para actualizar solo un campo tambien, aunqu epara eso mejor usar PATCH
@router.put("/")
async def user(user: User):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True   
            
    if not found:
            return {"error": "no se ha actualizado el usuario"}
        
    return user

@router.delete("/{id}")
async def user(id: int):

    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True 
    
    if not found:
            return {"error": "no se ha eliminado el usuario"}
        
    return {"msg" : "usuario eliminado"}