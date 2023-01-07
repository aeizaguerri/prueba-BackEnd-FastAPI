from fastapi import FastAPI

app = FastAPI()

#El get es una funcion dentro del protocolo https, y lo que hace es pedir algo a una URL

#Siempre que se llama a un servidor la funcion tiene que ser asincrona, lo que significa que el programa puede funcionar mientras 
#espera a que la funcion reciba respuesta del servidor

@app.get("/") #/ a secas es la raiz de la IP donde se despliega l app
async def root():
    return {"message": "Hola FastAPI"}
