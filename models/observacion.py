from db import db
from datetime import datetime
from models.profesor import Profesor
from models.alumno import Alumno

TIPOS_OBSERVACION = [
    ("OBSERVACION_PROFESOR", "OBSERVACION_PROFESOR"),
    ("OBSERVACION_ALUMNO", "OBSERVACION_ALUMNO"),
    ]
class Observacion(db.Document):
    titulo = db.StringField(max_length=30)
    contenido = db.StringField(max_length=200)
    tipo = db.StringField(choices=TIPOS_OBSERVACION)
    profesor = db.ReferenceField(Profesor)
    alumno = db.ReferenceField(Alumno)