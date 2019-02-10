from django.db import models

class TipoEvaluacion(models.Model):
    nombre = models.CharField(max_length = 40)
    cantidad_preguntas = models.IntegerField()