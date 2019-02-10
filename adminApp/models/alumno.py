from django.db import models
from adminApp.models.curso import Curso
from adminApp.models.apoderado import Apoderado
from adminApp.models.direccion import Direccion
from adminApp.models.colegio import Colegio

class Alumno(models.Model):
    nombres = models.CharField(max_length = 30)
    apellido_paterno = models.CharField(max_length = 15)
    apellido_materno = models.CharField(max_length = 15)
    rut = models.CharField(max_length = 10)
    email = models.EmailField(max_length = 254)
    telefono = models.CharField(max_length = 15)
    fecha_ingreso = models.DateTimeField(auto_now=True)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length = 10)
    imagen = models.ImageField()
    puntaje_ingreso = models.IntegerField(default=0)
    curso = models.ForeignKey(Curso, null=True, on_delete = models.SET_NULL)
    apoderado = models.ForeignKey(Apoderado, null=True, on_delete = models.SET_NULL)
    direccion = models.ForeignKey(Direccion, null=True, on_delete = models.SET_NULL)
    colegio = models.ForeignKey(Colegio, null=True, on_delete=models.SET_NULL)
    es_activo = models.BooleanField(default = True)
    contrasenna = models.CharField(max_length = 10)