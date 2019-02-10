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
from adminApp.models.justificacion import Justificacion
from adminApp.models.asignatura import Asignatura
from adminApp.models.evaluacion import Evaluacion
from adminApp.models.tipo_evaluacion import TipoEvaluacion
from adminApp.models.profesor import Profesor
from adminApp.models.observacion_docente import ObservacionDocente
from adminApp.models.pregunta import Pregunta
from adminApp.models.topico import Topico
from adminApp.models.anotacion import Anotacion
from adminApp.models.administrador import Administrador
from adminApp.models.noticia import Noticia

admin.site.register(Noticia)
admin.site.register(Administrador)
admin.site.register(Anotacion)
admin.site.register(Topico)
admin.site.register(Pregunta)
admin.site.register(ObservacionDocente)
admin.site.register(Profesor)
admin.site.register(TipoEvaluacion)
admin.site.register(Evaluacion)
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
