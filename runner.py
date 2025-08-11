import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.scrapers.compu_cordoba import scrape_compu_cordoba
from app.scrapers.venex import scrape_venex

# --- Configuración de MongoDB ---
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "scrapers_db"
COLLECTION_NAME = "productos"

def get_db_collection():
    """Se conecta a MongoDB y devuelve la colección de productos."""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ismaster') # Forzar conexión para verificar
        print("¡Conexión a MongoDB exitosa desde el runner!")
        db = client[DB_NAME]
        return db[COLLECTION_NAME]
    except ConnectionFailure as e:
        print(f"ERROR CRÍTICO: No se pudo conectar a MongoDB desde el runner. Detalle: {e}")
        return None

def almacenar(productos, fuente, coleccion):
    """Almacena una lista de productos en la colección de MongoDB."""
    if not productos:
        print(f"[{fuente}] No hay productos para almacenar.")
        return

    try:
        # Opcional: Borrar datos antiguos de la misma fuente para no duplicar
        # coleccion.delete_many({"fuente": fuente})

        # Añadir la fuente a cada producto antes de insertar
        for p in productos:
            p['fuente'] = fuente

        result = coleccion.insert_many(productos)
        print(f"[{fuente}] ➡️ {len(result.inserted_ids)} productos guardados en MongoDB.")
    except Exception as e:
        print(f"[{fuente}] ❌ Error guardando en MongoDB:", e)

if __name__ == "__main__":
    productos_collection = get_db_collection()

    if productos_collection is not None:
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
            except Exception as e:
                print(f"❌ Error ejecutando scraper {nombre}:", e)
            print("=" * 60)
            time.sleep(2) # Pequeña pausa entre scrapers