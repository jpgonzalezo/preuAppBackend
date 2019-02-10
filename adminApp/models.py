from django.db import models

class Region(models.Model):
    nombre = models.CharField(max_length = 30)

class Ciudad(models.Model):
    nombre = models.CharField(max_length = 30)
    region = models.ForeignKey(Region, null=True, on_delete = models.SET_NULL)

class Comuna(models.Model):
    nombre = models.CharField(max_length = 30)
    ciudad = models.ForeignKey(Ciudad, null=True, on_delete = models.SET_NULL)

class Direccion(models.Model):
    calle = models.CharField(max_length = 30)
    numero = models.IntegerField()
    comuna = models.ForeignKey(Comuna, null=True, on_delete = models.SET_NULL)

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







