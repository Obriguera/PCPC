import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# --- Configuración de MongoDB ---
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "scrapers_db"
COLLECTION_NAME = "productos"
productos_collection = None

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ismaster')
    db = client[DB_NAME]
    productos_collection = db[COLLECTION_NAME]
    print("¡Conexión a MongoDB exitosa!")
except ConnectionFailure as e:
    print(f"ERROR CRÍTICO: No se pudo conectar a MongoDB. {e}")

# --- Configuración de Gemini ---
# Carga la clave de forma segura desde las variables de entorno
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    # Si la clave no se encuentra, la aplicación no podrá iniciar.
    # Esto es mejor que fallar en medio de una petición.
    raise ValueError("No se encontró la variable de entorno GOOGLE_API_KEY. Asegúrate de crear el archivo .env y definirla.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# --- Modelos Pydantic ---
class Producto(BaseModel):
    nombre: str
    precio: str
    fuente: Optional[str] = None

class SearchRequest(BaseModel):
    necesidades: str
    presupuesto_max: Optional[int] = None

class SearchResponse(BaseModel):
    recomendacion: str
    producto_sugerido: Optional[Producto] = None

# --- Endpoints de la API ---

@app.get("/productos", response_model=List[Producto])
def listar_productos():
    """Devuelve todos los productos de la base de datos."""
    if not productos_collection:
        raise HTTPException(status_code=503, detail="Servicio no disponible (DB)")

    try:
        productos_db = list(productos_collection.find({}, {"_id": 0}))
        return productos_db
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer de la base de datos: {e}")

@app.post("/search", response_model=SearchResponse)
def buscar_con_ia(request: SearchRequest):
    """
    Recibe las necesidades y presupuesto del usuario, consulta la DB
    y usa una IA para recomendar la mejor notebook.
    """
    if not productos_collection:
        raise HTTPException(status_code=503, detail="Servicio no disponible (DB)")

    # 1. Obtener todos los productos de la base de datos
    try:
        lista_productos = list(productos_collection.find({}, {"_id": 0}))
        if not lista_productos:
            return SearchResponse(recomendacion="No se encontraron notebooks en la base de datos para analizar.", producto_sugerido=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar la base de datos: {e}")

    # 2. Construir el prompt para la IA
    prompt = f"""
    Eres un experto en hardware de computadoras que ayuda a usuarios a elegir la mejor notebook.
    Analiza la siguiente lista de productos disponibles y elige la MEJOR opción para un usuario según sus necesidades y presupuesto.

    **Necesidades del usuario:** "{request.necesidades}"
    **Presupuesto máximo:** ${request.presupuesto_max if request.presupuesto_max else "No especificado"}

    **Instrucciones:**
    1. Revisa CUIDADOSAMENTE cada producto de la lista. Considera que el precio está en pesos argentinos.
    2. Considera el nombre del producto para inferir sus componentes (CPU, RAM, almacenamiento, etc.).
    3. Elige solo UN producto, el que consideres la mejor opción.
    4. Tu respuesta DEBE ser un objeto JSON válido con dos claves: "razonamiento" (una explicación breve y amigable de por qué elegiste ese producto) y "nombre_producto" (el nombre exacto del producto que seleccionaste de la lista).
    5. No incluyas nada más en tu respuesta, solo el JSON.

    **Lista de productos disponibles:**
    {json.dumps(lista_productos, indent=2)}

    **Tu respuesta (solo el objeto JSON):**
    """

    # 3. Llamar a la IA de Gemini
    try:
        print("Enviando prompt a Gemini...")
        response = model.generate_content(prompt)
        
        # Limpiar y parsear la respuesta JSON de la IA
        ia_json_str = response.text.strip().replace("`", "").replace("json", "")
        ia_data = json.loads(ia_json_str)

        razonamiento = ia_data.get("razonamiento", "La IA no proporcionó una razón.")
        nombre_elegido = ia_data.get("nombre_producto")

        # 4. Buscar el producto recomendado en nuestra lista para devolverlo completo
        producto_elegido = next((p for p in lista_productos if p.get('nombre') == nombre_elegido), None)

        return SearchResponse(
            recomendacion=razonamiento,
            producto_sugerido=Producto(**producto_elegido) if producto_elegido else None
        )

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error: La IA no devolvió un JSON válido.")
    except Exception as e:
        print(f"Error al procesar la respuesta de la IA: {e}")
        raise HTTPException(status_code=500, detail="Error al comunicarse con el servicio de IA.")