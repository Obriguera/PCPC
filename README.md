# PCPC
Repo para el proyecto de Laboratorio 4 (2025). La aplicación recopilará precios de notebooks de diferentes página y las mostrará
en una página que además permitira encontrar la mejor PC para los requerimientos del usuario. 

# IDEAS
-Permitir cargar un presupuesto para que la IA lo tenga en cuenta
-Si llegamos a tener en cuenta componentes y no solamente Notebooks, ver que los componentes sean compatibles entre sí a la hora de armar una computadora

## Requisitos

* Python 3.12.X  

## Instalación
1. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
1. From where the project root directory is located.

2. Run the development server with:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Open your browser and go to `http://127.0.0.1:8000/` to see `{"message": "Hello, World!"}`.


# PCPC
Repositorio para el proyecto de Laboratorio 4 (2025). La aplicación recopila precios de notebooks de diferentes páginas, los almacena en una base de datos MongoDB y utiliza una IA (Gemini) para recomendar la mejor opción al usuario según sus necesidades.

# Ideas Implementadas
- **Base de Datos Centralizada**: Los datos de los scrapers se guardan en una base de datos MongoDB.
- **Búsqueda con IA**: Un endpoint permite a un usuario describir sus necesidades y presupuesto, y la IA de Google (Gemini) analiza los productos en la base de datos para ofrecer una recomendación inteligente.

## Requisitos
* Python 3.12.X
* MongoDB instalado y corriendo localmente.

## Instalación
1. Clona el repositorio y crea un entorno virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate



# PCPC - Comparador Inteligente de Notebooks
PCPC es un proyecto desarrollado para la cátedra de Laboratorio 4 (2025). La aplicación web está diseñada para centralizar precios de notebooks de diversos sitios de e-commerce, permitiendo a los usuarios encontrar la opción que mejor se adapte a sus necesidades y presupuesto mediante el uso de Inteligencia Artificial.

# 🚀 Características Principales
Scraping Multisitio: Recopilación automática de precios y especificaciones de notebooks de diferentes páginas web.

-Base de Datos Centralizada: Almacenamiento eficiente de productos en MongoDB.
-Asistente con IA (Gemini): Integración con la IA de Google para analizar el catálogo y recomendar la mejor PC basada en requerimientos técnicos y presupuesto del usuario.
-Análisis de Compatibilidad: (En desarrollo) Verificación de compatibilidad entre componentes para armado de PCs de escritorio.

# 🛠️ Requisitos Previos
```bash
Python 3.12.X
```
```bash
MongoDB (Instalado y ejecutándose localmente o en la nube)
```
Una API Key de Google Gemini (si se desea utilizar la funcionalidad de IA)

# 📦 Instalación
Clonar el repositorio:

```bash

git clone https://github.com/tu-usuario/PCPC.git
cd PCPC
Crear y activar un entorno virtual:
```

```bash

python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
Instalar las dependencias:
```

```bash
pip install -r requirements.txt
```
# ⚙️ Ejecución

```bash
uvicorn app.main:app --reload
```
Una vez iniciado, puedes acceder a la aplicación en:

Web: http://127.0.0.1:8000/

Documentación API (Swagger): http://127.0.0.1:8000/docs

Nota: Revisar de configurar las variables de entorno antes de iniciar el servidor.
