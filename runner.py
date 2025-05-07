import requests  # Import requests library
from app.scrapers.compu_cordoba import scrape_compu_cordoba
from app.scrapers.venex import scrape_venex

API_URL = "http://127.0.0.1:8000/productos"

def enviar(productos, fuente):
    for p in productos:
        try:
            # Ensure 'nombre' exists in the product dictionary
            nombre = p.get('nombre', 'Producto sin nombre')
            resp = requests.post(API_URL, json=p)
            print(f"[{fuente}] ➡️ Enviado {nombre} - {resp.status_code}")
        except Exception as e:
            print(f"[{fuente}] ❌ Error enviando {nombre}:", e)

if __name__ == "__main__":
    scrapers = [
        ("compu_cordoba", scrape_compu_cordoba),
        ("venex", scrape_venex),
    ]

    for nombre, funcion in scrapers:
        print(f"🔍 Ejecutando scraper: {nombre}")
        try:
            resultados = funcion()
            print(f"   {len(resultados)} resultados de {nombre}")
            enviar(resultados, nombre)
        except Exception as e:
            print(f"❌ Error ejecutando scraper {nombre}:", e)
        print("=" * 60)