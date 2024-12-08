# Proyecto de Automatización de Procesos con Django

Este proyecto permite automatizar la lectura de un archivo Excel, procesar los datos y enviarlos a una API externa. Incluye autenticación, manejo de errores y una interfaz para cargar manualmente archivos desde el frontend.

## Requisitos Previos

- Python 3.8 o superior
- Django 4.x
- Un entorno virtual (recomendado)

## Instalación

1. Clona este repositorio en tu máquina local:
 
   git clone https://github.com/usuario/proyecto-django.git](https://github.com/TecnoparqueRionegroLineaVirtuales/apialagro/ 
   cd agro

2. Crea y activa un entorno virtual:

python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate

3. Instala las dependencias del proyecto:

pip install -r requirements.txt
Configura la base de datos y aplica las migraciones:

python manage.py makemigrations
python manage.py migrate

4. Configuración
Asegúrate de que la carpeta media existe en el directorio base del proyecto. Si no existe, créala manualmente:

mkdir media
Coloca tu archivo alagro.xlsx en la carpeta media.

5. Crear Usuario Administrador
Ejecuta el siguiente comando para crear un usuario administrador:

python manage.py createsuperuser --email admin@mail.com --username admin
Cuando se te solicite, usa las siguientes credenciales:

Email: admin@mail.com
Contraseña: 123456

6. Ejecución del Proyecto
Inicia el servidor de desarrollo:

python manage.py runserver
Accede al proyecto en tu navegador en http://127.0.0.1:8000.

Endpoints Principales
Cargar Archivo Manualmente: http://127.0.0.1:8000/cargar-archivo/

Permite cargar un archivo Excel manualmente desde el navegador.
Procesar Archivo Automáticamente: http://127.0.0.1:8000/procesar-automatico/

Busca el archivo alagro.xlsx en la carpeta media, lo procesa y envía los datos a la API externa.

7. Logs
Los mensajes del proceso se registran en la consola para facilitar el monitoreo del flujo y manejo de errores.
