from django.db import models
from adminApp.models.tipo_evaluacion import TipoEvaluacion
from adminApp.models.asignatura import Asignatura
from adminApp.models.alumno import Alumno

class Evaluacion(models.Model):
    nombre = models.CharField(max_length = 40)
    tipo = models.ForeignKey(TipoEvaluacion, null=True, on_delete = models.SET_NULL)
    cantidad_buenas = models.IntegerField()
    cantidad_malas = models.IntegerField()
    cantidad_omitidas = models.IntegerField()
    puntaje = models.IntegerField()
    asignatura = models.ForeignKey(Asignatura, null=True, on_delete = models.SET_NULL)
    alumno = models.ForeignKey(Alumno, null=True, on_delete = models.SET_NULL)
    fecha = models.DateField()