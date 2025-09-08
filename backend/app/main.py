from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import os

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MongoDB ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/scrapers_db")
client = MongoClient(MONGO_URI)
db = client.scrapers_db
productos_col = db.productos

# --- Modelo Pydantic ---
class Producto(BaseModel):
    nombre: str
    precio: str
    fuente: str | None = None

# --- Rutas ---
@app.post("/productos")
def recibir_producto(producto: Producto):
    doc = producto.dict()
    productos_col.insert_one(doc)
    return {"mensaje": "Producto recibido"}

@app.get("/productos")
def listar_productos():
    productos = list(productos_col.find({}, {"_id": 0}))  # excluir ObjectId
    return productos
