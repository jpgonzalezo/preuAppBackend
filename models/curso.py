from db import db
from datetime import datetime
from models.pregunta import Pregunta
from models.asignatura import Asignatura
from models.institucion import Institucion
from models.alumno import Alumno
 
import mongoengine_goodjson as gj
class Curso(gj.Document):
    nombre = db.StringField(verbose_name="Nombre curso", max_length=200)
    fecha_creacion = db.DateTimeField(default=datetime.now)
    preguntas = db.ListField(db.EmbeddedDocumentField(Pregunta))
    asignatura = db.ReferenceField(Asignatura)
    institucion = db.ReferenceField(Institucion)
    alumnos = db.ListField(db.ReferenceField(Alumno))
    meta = {'strict': False}