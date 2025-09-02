import time
import os
import requests  # type: ignore
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.scrapers.compu_cordoba import scrape_compu_cordoba
from app.scrapers.venex import scrape_venex

# --- Configuración de FastAPI ---
API_URL = os.getenv("API_URL", "http://fastapi:8000/productos")  # usar nombre del servicio en Docker

# --- Configuración de MongoDB ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/scrapers_db")
DB_NAME = "scrapers_db"
COLLECTION_NAME = "productos"

def get_db_collection():
    """Se conecta a MongoDB y devuelve la colección de productos."""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ismaster')  # Forzar conexión para verificar
        print("¡Conexión a MongoDB exitosa desde el runner!")
        db = client[DB_NAME]
        return db[COLLECTION_NAME]
    except ConnectionFailure as e:
        print(f"ERROR CRÍTICO: No se pudo conectar a MongoDB desde el runner. Detalle: {e}")
        return None

def almacenar(productos, fuente, coleccion):
    """Almacena una lista de productos en MongoDB."""
    if not productos:
        print(f"[{fuente}] No hay productos para almacenar.")
        return

    try:
        for p in productos:
            p['fuente'] = fuente
        result = coleccion.insert_many(productos)
        print(f"[{fuente}] ➡️ {len(result.inserted_ids)} productos guardados en MongoDB.")
    except Exception as e:
        print(f"[{fuente}] ❌ Error guardando en MongoDB:", e)

def enviar(productos, fuente):
    """Envía los productos a la API de FastAPI."""
    for p in productos:
        try:
            nombre = p.get('nombre', 'Producto sin nombre')
            resp = requests.post(API_URL, json=p)
            print(f"[{fuente}] ➡️ Enviado {nombre} - {resp.status_code}")
        except Exception as e:
            print(f"[{fuente}] ❌ Error enviando {nombre}:", e)

if __name__ == "__main__":
    productos_collection = get_db_collection()

    scrapers = [
        ("compu_cordoba", scrape_compu_cordoba),
        ("venex", scrape_venex),
    ]

    for nombre, funcion in scrapers:
        print(f"🔍 Ejecutando scraper: {nombre}")
        try:
            resultados = funcion()
            print(f"   {len(resultados)} resultados de {nombre}")

            # --- Guardar en MongoDB ---
            if productos_collection:
                almacenar(resultados, nombre, productos_collection)

            # --- Enviar a FastAPI ---
            enviar(resultados, nombre)

        except Exception as e:
            print(f"❌ Error ejecutando scraper {nombre}:", e)

        print("=" * 60)
        time.sleep(2)  # Pausa entre scrapers
