from django.contrib import admin
from adminApp.models import Alumno
from adminApp.models import Apoderado
from adminApp.models import Curso
from adminApp.models import Colegio
from adminApp.models import Direccion
from adminApp.models import Comuna
from adminApp.models import Ciudad
from adminApp.models import Region
from adminApp.models import Asistencia
from adminApp.models import Justificacion

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
