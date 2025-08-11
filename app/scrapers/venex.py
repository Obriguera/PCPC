from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import re

BASE_URL = "https://www.venex.com.ar/notebooks?cPath=249&page={}"

def get_max_page(driver):
    """Detecta la última página del paginador en Venex"""
    driver.get(BASE_URL.format(1))
    time.sleep(2)
    elementos = driver.find_elements(By.CSS_SELECTOR, "a.pageResults")
    paginas = []

    for el in elementos:
        texto = el.text.strip()
        if texto.isdigit():
            paginas.append(int(texto))

    return max(paginas) if paginas else 1

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    
    # Le decimos a Selenium que use el archivo .exe de la carpeta del proyecto
    service = Service(executable_path="chromedriver.exe")
    
    return webdriver.Chrome(service=service, options=options)

def extract_json_from_onclick(onclick_attr):
    # Extrae JSON de: onclick="enhancedClick({...})"
    match = re.search(r"enhancedClick\((\{.*?\})\)", onclick_attr)
    if match:
        json_str = match.group(1)
        # Reemplazamos entidades HTML y comillas escapadas
        json_str = json_str.replace("&quot;", "\"").replace("\\\"", "\"")
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None

def scrape_venex():
    driver = get_driver()
    productos = []

    max_page = get_max_page(driver)
    print(f"[venex] Se detectaron {max_page} páginas.")

    for page in range(1, max_page + 1):
        url = BASE_URL.format(page)
        print(f"[venex] Visitando página {page}: {url}")
        driver.get(url)
        time.sleep(2)

        links = driver.find_elements(By.CSS_SELECTOR, "a.product-box-overlay")
        if not links:
            print(f"[venex] Página {page} vacía.")
            continue

        for link in links:
            onclick = link.get_attribute("onclick")
            data = extract_json_from_onclick(onclick)
            if data:
                nombre = data.get("name", "Sin nombre")
                precio = f"${data.get('price', '0')}"
                productos.append({"nombre": nombre, "precio": precio})
                print(f"📦 {nombre} | 💲 {precio}")

        time.sleep(1)

    driver.quit()
    return productos
