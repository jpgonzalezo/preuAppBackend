from django.db import models
from adminApp.models.direccion import Direccion

class Administrador(models.Model):
    nombres = models.CharField(max_length = 30)
    apellido_paterno = models.CharField(max_length = 15)
    apellido_materno = models.CharField(max_length = 15)
    rut = models.CharField(max_length = 10)
    email = models.EmailField(max_length = 254)
    telefono = models.CharField(max_length = 15)
    imagen = models.ImageField()
    direccion = models.ForeignKey(Direccion, null=True, on_delete = models.SET_NULL)
    contrasenna = models.CharField(max_length = 10)