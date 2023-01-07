from fastapi import FastAPI
from pydantic import BaseModel

#lanza el servidor utilizando el comando uvicorn users:app -- reload (acuerdate de guardar antes para que funcione)
app = FastAPI()

#Creando una entidad utlizando BaseModel, se interpreta conmo un JSON por FastAPI
class User(BaseModel):
    id : int
    name : str
    surname : str
    url : str
    age : int

users_list = [
    User(id = 1, name = "Alberto", surname = "Eiza",url =  "aeiza.com",age = 24),
    User(id = 2, name = "Juan", surname = "Eiza",url =  "jeiza.com",age = 20)
    ]

#Busqueda de usuarios en la db fake y manejo de errores
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario con el id"}

#Saca toda la lista de usuarios de una supuesta db fake
@app.get("/users")
async def users():
    return users_list

#Saca solo el usuario que se le indique en la url
@app.get("/users/{id}")
async def user(id : int):
    return search_user(id)

#Saca el usuario utilizando query
#Poniendo ./?{parametro}=x en la url pasas el valor x directamente a la funcion
@app.get("/userquery")
async def user(id : int):
    return search_user(id)