from django.urls import path
from . import views

urlpatterns = [
    path('cargar-archivo/', views.cargar_archivo, name='cargar_archivo'),
    path('archivo-exitoso/', views.archivo_exitoso, name='archivo_exitoso'),
    path('procesar-automatico/', views.procesar_archivo_automatico, name='procesar_automatico'),
]
