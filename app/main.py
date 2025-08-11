from fastapi import FastAPI, HTTPException # Importar HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure # Errores específicos de MongoDB
from typing import List

app = FastAPI()

# --- Configuración de MongoDB ---
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "scrapers_db"
COLLECTION_NAME = "productos"

client = None
db = None
productos_collection = None

try:
    print(f"Intentando conectar a MongoDB en {MONGO_URI}...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000) # Timeout para la conexión
    # Verificar la conexión intentando obtener información del servidor
    client.admin.command('ismaster')
    print("¡Conexión a MongoDB exitosa!")
    db = client[DB_NAME]
    productos_collection = db[COLLECTION_NAME]
    print(f"Usando base de datos '{DB_NAME}' y colección '{COLLECTION_NAME}'.")
except ConnectionFailure as e:
    print(f"ERROR CRÍTICO: No se pudo conectar a MongoDB. Asegúrate de que esté corriendo. Detalle: {e}")
    # El servidor FastAPI seguirá corriendo, pero las operaciones de DB fallarán.
    # Podrías decidir terminar la app aquí si MongoDB es esencial:
    # import sys
    # sys.exit("No se pudo conectar a MongoDB.")
except Exception as e:
    print(f"ERROR CRÍTICO INESPERADO durante la conexión a MongoDB: {e}")

class Producto(BaseModel):
    nombre: str
    precio: str

@app.post("/productos")
def recibir_producto(producto: Producto):
    if not productos_collection:
        print("ERROR en POST /productos: La colección de MongoDB no está disponible (falló la conexión inicial).")
        raise HTTPException(status_code=503, detail="Servicio no disponible debido a un problema con la base de datos.")

    producto_dict = producto.model_dump()
    print(f"\n--- Endpoint POST /productos ---")
    print(f"RECIBIDO: {producto_dict}")
    try:
        print("Intentando insertar en MongoDB...")
        result = productos_collection.insert_one(producto_dict)
        print(f"PRODUCTO GUARDADO en MongoDB. ID: {result.inserted_id}")
        print(f"-----------------------------\n")
        return {"mensaje": "Producto recibido y guardado en MongoDB", "id_insertado": str(result.inserted_id)}
    except OperationFailure as e:
        print(f"ERROR DE OPERACIÓN AL GUARDAR EN MONGODB: {e.details}") # .details puede dar más info
        print(f"-----------------------------\n")
        raise HTTPException(status_code=500, detail=f"Error al guardar en la base de datos: {e.details}")
    except Exception as e:
        print(f"ERROR INESPERADO AL GUARDAR EN MONGODB: {e}")
        print(f"-----------------------------\n")
        raise HTTPException(status_code=500, detail=f"Error interno inesperado al guardar el producto: {str(e)}")

@app.get("/productos", response_model=List[Producto])
def listar_productos():
    if not productos_collection:
        print("ERROR en GET /productos: La colección de MongoDB no está disponible.")
        raise HTTPException(status_code=503, detail="Servicio no disponible debido a un problema con la base de datos.")

    productos_desde_db = []
    print(f"\n--- Endpoint GET /productos ---")
    try:
        print("Intentando leer productos de MongoDB...")
        for p_doc in productos_collection.find({}, {"_id": 0}):
            productos_desde_db.append(Producto(**p_doc))
        print(f"PRODUCTOS LEÍDOS DE MONGODB: {len(productos_desde_db)} encontrados.")
        print(f"----------------------------\n")
        return productos_desde_db
    except OperationFailure as e:
        print(f"ERROR DE OPERACIÓN AL LEER DE MONGODB: {e.details}")
        print(f"----------------------------\n")
        raise HTTPException(status_code=500, detail=f"Error al leer de la base de datos: {e.details}")
    except Exception as e:
        print(f"ERROR INESPERADO AL LEER DE MONGODB: {e}")
        print(f"----------------------------\n")
        raise HTTPException(status_code=500, detail=f"Error interno inesperado al leer productos: {str(e)}")

# (Opcional: /productos_raw - recuerda agregar manejo de errores similar si lo usas)
@app.get("/productos_raw")
def listar_productos_raw():
    if not productos_collection:
        raise HTTPException(status_code=503, detail="MongoDB collection not available.")
    try:
        productos_crudos = list(productos_collection.find())
        for p in productos_crudos:
            p["_id"] = str(p["_id"]) # Convertir ObjectId a string
        return productos_crudos
    except Exception as e:
        print(f"Error en /productos_raw: {e}")
        raise HTTPException(status_code=500, detail="Error fetching raw products.")