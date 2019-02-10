from django.db import models
from adminApp.models.region import Region

class Ciudad(models.Model):
    nombre = models.CharField(max_length = 30)
    region = models.ForeignKey(Region, null=True, on_delete = models.SET_NULL)