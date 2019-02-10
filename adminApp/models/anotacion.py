from django.db import models
from adminApp.models.alumno import Alumno

class Anotacion (models.Model):
    titulo = models.CharField(max_length = 40)
    detalle = models.CharField(max_length = 300)
    rut = models.CharField(max_length = 10)
    fecha = models.DateTimeField(auto_now=True)
    alumno = models.ForeignKey(Alumno, null=True, on_delete = models.SET_NULL)