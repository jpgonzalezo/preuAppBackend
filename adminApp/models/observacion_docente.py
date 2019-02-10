from django.db import models
from adminApp.models.profesor import Profesor

class ObservacionDocente(models.Model):
    titulo = models.CharField(max_length = 40)
    detalle = models.CharField(max_length = 300)
    rut = models.CharField(max_length = 10)
    fecha = models.DateTimeField(auto_now=True)
    profesor = models.ForeignKey(Profesor, null=True, on_delete = models.SET_NULL)