from django.db import models

class ArchivoEntrada(models.Model):
    archivo = models.FileField(upload_to='archivos_excel/')
    fecha_carga = models.DateTimeField(auto_now_add=True)

class EntradaDato(models.Model):
    time = models.DateTimeField()
    temperatura = models.FloatField()
    volumen = models.FloatField()
    distancia = models.FloatField()
    state = models.BooleanField(default=False)  
