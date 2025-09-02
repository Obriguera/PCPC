import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")

    if os.getenv("RUNNING_IN_DOCKER"):
        print("DEBUG: Usando Chromedriver para Docker.")
        service = Service(executable_path="/usr/bin/chromedriver")
    else:
        print("DEBUG: Usando Chromedriver para entorno local (webdriver_manager).")
        service = Service(ChromeDriverManager().install())
    
    return webdriver.Chrome(service=service, options=options)

def scrape_compu_cordoba():
    """Scrapea notebooks de compucordoba.com.ar/notebooks"""
    driver = get_driver()
    driver.get("https://compucordoba.com.ar/notebooks")
    
    # Dale tiempo al JS para renderizar
    time.sleep(5)

    elems = driver.find_elements(By.CLASS_NAME, "product-card")
    print(f"[compu_cordoba] Productos encontrados: {len(elems)}")

    products = []
    for el in elems:
        try:
            nombre = el.find_element(By.CLASS_NAME, "product-card__name").text
        except:
            nombre = "Nombre no encontrado"
        try:
            precio = el.find_element(By.CLASS_NAME, "product-card__prices").text
        except:
            precio = "Precio no disponible"

        # Imprime igual que tu scraper original
        print("📦 Producto:", nombre)
        print("💲 Precio:", precio)
        print("-" * 40)

        products.append({
            "nombre": nombre,
            "precio": precio
        })

    driver.quit()
    return products