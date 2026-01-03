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
