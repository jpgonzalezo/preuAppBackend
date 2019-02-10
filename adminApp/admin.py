from django.contrib import admin
from adminApp.models.alumno import Alumno
from adminApp.models.apoderado import Apoderado
from adminApp.models.curso import Curso
from adminApp.models.colegio import Colegio
from adminApp.models.direccion import Direccion
from adminApp.models.comuna import Comuna
from adminApp.models.ciudad import Ciudad
from adminApp.models.region import Region
from adminApp.models.asistencia import Asistencia
from adminApp.models.justificaion import Justificacion
from adminApp.models.asignatura import Asignatura

admin.site.register(Asignatura)
admin.site.register(Alumno)
admin.site.register(Apoderado)
admin.site.register(Curso)
admin.site.register(Colegio)
admin.site.register(Direccion)
admin.site.register(Comuna)
admin.site.register(Ciudad)
admin.site.register(Region)
admin.site.register(Asistencia)
admin.site.register(Justificacion)

# Register your models here.
