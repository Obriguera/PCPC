from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Producto(BaseModel):
    nombre: str
    precio: str

productos_recibidos = []

@app.post("/productos")
def recibir_producto(producto: Producto):
    productos_recibidos.append(producto)
    return {"mensaje": "Producto recibido"}

@app.get("/productos")
def listar_productos():
    return productos_recibidos
