from django.db import models

class Colegio(models.Model):
    nombre = models.CharField(max_length = 30)
    direccion = models.ForeignKey(Direccion, null=True, on_delete = models.SET_NULL)

class Apoderado(models.Model):
    nombres = models.CharField(max_length = 30)
    apellido_paterno = models.CharField(max_length = 15)
    apellido_materno = models.CharField(max_length = 15)
    rut = models.CharField(max_length = 10)
    email = models.EmailField(max_length = 254)
    telefono = models.CharField(max_length = 15)
    fecha_ingreso = models.DateTimeField(auto_now=True)
    imagen = models.ImageField()
    direccion = models.ForeignKey(Direccion, null=True, on_delete = models.SET_NULL)
    es_activo = models.BooleanField(default = True)

class Curso(models.Model):
    nombre = models.CharField(max_length = 15)
    annio = models.IntegerField()
    es_activo = models.BooleanField(default = True)


class Asignatura(models.Model):
    nombre = models.CharField(max_length = 15)

class Asistencia(models.Model):
    fecha = models.DateField(auto_now=True)
    asignatura = models.ForeignKey(Asignatura, null=True, on_delete = models.SET_NULL)
    alumno = models.ForeignKey(Alumno, null=True, on_delete = models.SET_NULL)
    esta_presente = models.BooleanField(default = True)

class Justificacion (models.Model):
    fecha = models.DateTimeField(auto_now=True)
    asistencia = models.ForeignKey(Asistencia, null=True, on_delete = models.CASCADE)
    observacion = models.EmailField(max_length = 300)







