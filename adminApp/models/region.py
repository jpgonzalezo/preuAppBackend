from django.db import models

class Region(models.Model):
    nombre = models.CharField(max_length = 60)