from django.db import models
from adminApp.models.topico import Topico
from adminApp.models.asignatura import Asignatura

class Pregunta(models.Model):
    alternativa = models.CharField(max_length = 1, null=True)
    alternativa_correcta = models.CharField(max_length = 1)
    topico = models.ForeignKey(Topico, null=True, on_delete = models.SET_NULL)
    asignatura = models.ForeignKey(Asignatura, null=True, on_delete = models.SET_NULL)