from django.db import models
from adminApp.models.direccion import Direccion

class Colegio(models.Model):
    nombre = models.CharField(max_length = 30)
    direccion = models.ForeignKey(Direccion, null=True, on_delete = models.SET_NULL)