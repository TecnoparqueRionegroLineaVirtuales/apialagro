import requests
import logging
import os
from django.conf import settings
from django.http import JsonResponse
import pandas as pd
from django.shortcuts import render, redirect
from .forms import ArchivoEntradaForm
from .models import ArchivoEntrada, EntradaDato

logger = logging.getLogger(__name__)


def procesar_archivo_automatico(request):
    archivo_path = os.path.join(settings.MEDIA_ROOT, "archivos_excel/alagro.xlsx")

    if not os.path.exists(archivo_path):
        logger.error(f"El archivo {archivo_path} no se encontró.")
        return JsonResponse({"status": "ERROR", "message": "Archivo no encontrado."}, status=404)

    try:
        # Procesando el archivo
        logger.info(f"Procesando archivo automatizado: {archivo_path}")
        procesar_excel(archivo_path)
        return JsonResponse({"status": "OK", "message": "Archivo procesado exitosamente."})
    except Exception as e:
        logger.error(f"Error al procesar el archivo: {e}")
        return JsonResponse({"status": "ERROR", "message": str(e)}, status=500)

def autenticar_api():
    url_login = "http://appalagro.com:4100/api/user/login"
    payload = {"password": "M&v72KYh@5"}
    try:
        logger.info("Iniciando autenticación con la API externa.")
        response = requests.post(url_login, json=payload)
        response.raise_for_status()  # Lanza un error si el código no es 200
        token = response.json().get("tokenJwt")
        if not token:
            logger.error("La respuesta no contiene un token válido.")
            raise ValueError("Token de autenticación no encontrado.")
        logger.info("Autenticación exitosa. Token obtenido.")
        return token
    except requests.exceptions.RequestException as e:
        logger.error(f"Error durante la autenticación: {e}")
        raise Exception("Error al autenticar con la API externa.") from e

def enviar_datos_api(data, token):
    url_add = "http://appalagro.com:4100/api/info/add"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        logger.info(f"Enviando datos a la API externa: {data}")
        response = requests.post(url_add, json=data, headers=headers)
        response.raise_for_status()
        logger.info(f"Datos enviados exitosamente. Respuesta: {response.json()}")
        return response.status_code, response.json()  
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al enviar datos: {e}")
        return None, {"status": "ERROR", "message": str(e)}

def cargar_archivo(request):
    if request.method == 'POST':
        form = ArchivoEntradaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save()
            procesar_excel(archivo.archivo.path)
            return redirect('archivo_exitoso')
    else:
        form = ArchivoEntradaForm()
    return render(request, 'cargar_archivo.html', {'form': form})


def procesar_excel(file_path):
    logger.info(f"Procesando archivo Excel: {file_path}")
    processed_data = pd.read_excel(
        file_path,
        sheet_name="Entrada de datos",
        header=6,
        usecols="A:D"
    )
    processed_data.dropna(how="all", inplace=True)
    processed_data.columns = ["TIME", "Temperatura(°C)", "Volumen (Lts)", "Distancia (cm)"]

    try:
        token = autenticar_api()
    except Exception as e:
        logger.error(f"No se pudo autenticar: {e}")
        return

    for index, row in processed_data.iterrows():
        entrada = EntradaDato.objects.create(
            time=row["TIME"],
            temperatura=row["Temperatura(°C)"],
            volumen=row["Volumen (Lts)"],
            distancia=row["Distancia (cm)"]
        )
        api_data = {
            "id": "111",  # ID del tanque fijo
            "volumen": str(entrada.volumen),
            "temp": str(entrada.temperatura),
            "datetime": entrada.time.strftime("%Y-%m-%d %H:%M:%S")
        }
        status_code, response_json = enviar_datos_api(api_data, token)
        
        if status_code == 200 and response_json.get("status") == "OK":
            entrada.state = True
            entrada.save()
            logger.info(f"Dato con ID {entrada.id} enviado correctamente. Respuesta del servidor: {response_json}")
        else:
            logger.error(f"Error al enviar dato con ID {entrada.id}. Respuesta del servidor: {response_json}")

def archivo_exitoso(request):
    return render(request, 'archivo_exitoso.html')
