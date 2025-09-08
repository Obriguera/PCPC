import time
import os
import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from app.scrapers.compu_cordoba import scrape_compu_cordoba
from app.scrapers.venex import scrape_venex

API_URL = os.getenv("API_URL", "http://fastapi:8000/productos")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/scrapers_db")
DB_NAME = "scrapers_db"
COLLECTION_NAME = "productos"

def get_db_collection(retries=10, delay=5):
    """Se conecta a MongoDB con retry loop."""
    for i in range(retries):
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.admin.command('ismaster')  # Verifica conexión
            print("✅ Conexión a MongoDB exitosa.")
            db = client[DB_NAME]
            return db[COLLECTION_NAME]
        except ConnectionFailure as e:
            print(f"⚠️ Intento {i+1}/{retries} - No se pudo conectar a MongoDB. Reintentando en {delay}s...")
            time.sleep(delay)
    print("❌ No se pudo conectar a MongoDB después de varios intentos.")
    return None

def almacenar(productos, fuente, coleccion):
    if not productos or coleccion is None:
        print(f"[{fuente}] No hay productos para almacenar o la colección no está disponible.")
        return
    for p in productos:
        p['fuente'] = fuente
    try:
        result = coleccion.insert_many(productos)
        print(f"[{fuente}] ➡️ {len(result.inserted_ids)} productos guardados en MongoDB.")
    except Exception as e:
        print(f"[{fuente}] ❌ Error guardando en MongoDB: {e}")

def enviar(productos, fuente, retries=5, delay=3):
    for p in productos:
        if "_id" in p:
            del p["_id"]
        nombre = p.get('nombre', 'Producto sin nombre')

        for i in range(retries):
            try:
                resp = requests.post(API_URL, json=p, timeout=5)
                if resp.ok:
                    print(f"[{fuente}] ➡️ Enviado {nombre} - {resp.status_code}")
                    break
                else:
                    raise Exception(f"Status {resp.status_code}")
            except Exception as e:
                print(f"[{fuente}] ⚠️ Error enviando {nombre} (intento {i+1}/{retries}): {e}")
                time.sleep(delay)

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

            almacenar(resultados, nombre, productos_collection)
            enviar(resultados, nombre)

        except Exception as e:
            print(f"❌ Error ejecutando scraper {nombre}: {e}")

        print("="*60)
        time.sleep(2)
