from django.db import models
from adminApp.models.administrador import Administrador

class Noticia(models.Model):
    titulo = models.CharField(max_length = 40)
    contenido = models.CharField(max_length = 500)
    imagen = models.ImageField()
    es_activo = models.BooleanField(default = True)
    administrador = models.ForeignKey(Administrador, null=True, on_delete = models.SET_NULL)