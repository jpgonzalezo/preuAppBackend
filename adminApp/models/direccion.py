from django.db import models
from adminApp.models.comuna import Comuna 

class Direccion(models.Model):
    calle = models.CharField(max_length = 30)
    numero = models.IntegerField()
    comuna = models.ForeignKey(Comuna, null=True, on_delete = models.SET_NULL)