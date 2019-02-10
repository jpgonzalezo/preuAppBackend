from django.db import models
from adminApp.models.ciudad import Ciudad

class Comuna(models.Model):
    nombre = models.CharField(max_length = 30)
    ciudad = models.ForeignKey(Ciudad, null=True, on_delete = models.SET_NULL)