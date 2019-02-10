from django.db import models
from adminApp.models.asignatura import Asignatura

class Curso(models.Model):
    nombre = models.CharField(max_length = 15)
    annio = models.IntegerField()
    es_activo = models.BooleanField(default = True)
    asignaturas = models.ManyToManyField(Asignatura)