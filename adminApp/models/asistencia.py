from django.db import models
from adminApp.models.asignatura import Asignatura
from adminApp.models.alumno import Alumno

class Asistencia(models.Model):
    fecha = models.DateField(auto_now=True)
    asignatura = models.ForeignKey(Asignatura, null=True, on_delete = models.SET_NULL)
    alumno = models.ForeignKey(Alumno, null=True, on_delete = models.SET_NULL)
    esta_presente = models.BooleanField(default = True)