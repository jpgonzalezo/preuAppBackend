from django.db import models
from adminApp.models.asistencia import Asistencia

class Justificacion (models.Model):
    fecha = models.DateTimeField(auto_now=True)
    asistencia = models.ForeignKey(Asistencia, null=True, on_delete = models.CASCADE)
    observacion = models.EmailField(max_length = 300)