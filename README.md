# PCPC
Repo para el proyecto de Laboratorio 4 (2025). La aplicación recopilará precios de notebooks de diferentes página y las mostrará
en una página que además permitira encontrar la mejor PC para los requerimientos del usuario. 

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
