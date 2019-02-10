from django.db import models
from adminApp.models.asignatura import Asignatura

class Topico(models.Model):
    nombre = models.CharField(max_length = 100)
    asignatura = models.ForeignKey(Asignatura, null=True, on_delete = models.SET_NULL)