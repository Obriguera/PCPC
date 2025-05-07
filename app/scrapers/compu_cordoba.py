# app/scrapers/compu_cordoba.py
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def get_driver():
    options = Options()
    options.add_argument("--headless")        # Ejecutar en segundo plano
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    # Si necesitás forzar la ruta de Chrome:
    # options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

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
