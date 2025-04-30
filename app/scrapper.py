from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests
import time

# Configuración del navegador
options = Options()
options.add_argument("--headless")  # Ejecutar en segundo plano
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

# Ruta opcional si no encuentra Chrome automáticamente (descomentar si da error)
# options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# Iniciar el navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = 'https://compucordoba.com.ar/notebooks'
driver.get(url)

# Esperar a que cargue el contenido
time.sleep(5)  # Ajustar si la página tarda más

# Extraer productos
productos = driver.find_elements(By.CLASS_NAME, 'product-card')
print("Productos encontrados:", len(productos))

# URL del endpoint FastAPI
API_URL = "http://127.0.0.1:8000/productos"  # Cambiar si tu API está en otro host o puerto

for producto in productos:
    try:
        nombre = producto.find_element(By.CLASS_NAME, 'product-card__name').text
    except:
        nombre = "Nombre no encontrado"

    try:
        precio = producto.find_element(By.CLASS_NAME, 'product-card__prices').text
    except:
        precio = "Precio no disponible"

    print("📦 Producto:", nombre)
    print("💲 Precio:", precio)

    # Enviar al backend
    data = {
        "nombre": nombre,
        "precio": precio
    }

    try:
        response = requests.post(API_URL, json=data)
        print("➡️ Enviado:", response.status_code)
    except Exception as e:
        print("❌ Error al enviar:", e)

    print("=" * 40)

driver.quit()
