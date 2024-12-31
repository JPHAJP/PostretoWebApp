# Web App para Crear Recibos y Modificar Menú de Productos

Esta es una aplicación web para una tienda local que permite crear recibos personalizados y modificar su menú de productos. La app utiliza **Flask** como backend (API), permite la creación de **recibos en formato PDF** y está desplegada en **Render**.

## Características

- Crear recibos de compras con productos seleccionados.
- Modificar el menú de productos que están disponibles para los recibos.
- Generación de recibos en formato PDF para ser descargados.
- Despliegue en Render para acceso en línea.

## Tecnologías Usadas

- **Flask**: Framework web para la API backend.
- **Gunicorn**: Servidor WSGI para ejecutar la app Flask en producción.
- **Render**: Plataforma de despliegue para alojar la aplicación.
- **ReportLab**: Librería de Python para generar PDFs de recibos.

## Instalación

### Requisitos

- **Python 3.7+**
- **pip** (para instalar las dependencias)

### Pasos para instalar localmente:

1. Clona este repositorio:

   ```bash
   git clone https://github.com/JPHAJP/PostretoWebApp.git
   cd /PostretoWebApp

2. Crea un entorno virtual:
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

3. Instala dependencias
  pip install -r requirements.txt

4. Ejecuta mediante python
   python3 app/app.py
