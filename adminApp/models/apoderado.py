from django.db import models
from adminApp.models.direccion import Direccion

class Apoderado(models.Model):
    nombres = models.CharField(max_length = 30)
    apellido_paterno = models.CharField(max_length = 15)
    apellido_materno = models.CharField(max_length = 15)
    rut = models.CharField(max_length = 10)
    email = models.EmailField(max_length = 254)
    telefono = models.CharField(max_length = 15)
    fecha_ingreso = models.DateTimeField(auto_now=True)
    imagen = models.ImageField()
    direccion = models.ForeignKey(Direccion, null=True, on_delete = models.SET_NULL)
    es_activo = models.BooleanField(default = True)