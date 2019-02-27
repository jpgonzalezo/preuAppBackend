from db import db
from datetime import datetime
from models.alumno import Alumno
from models.curso import Curso
from models.historial import Historial

TIPOS_ESTADO_INSCRIPCION = [
    ("ENVIADA", "ENVIADA"),
    ("REVISION", "REVISION"),
    ("ACEPTADA", "ACEPTADA"),
    ("RECHAZADA", "RECHAZADA")
    ]

class Inscripcion(db.Document):
    alumno = db.ReferenceField(Alumno)
    curso = db.ReferenceField(Curso)
    estado = db.StringField(choices=TIPOS_ESTADO_INSCRIPCION)
    historial = db.ListField(db.EmbeddedDocumentField(Historial))
    meta = {'strict': False}