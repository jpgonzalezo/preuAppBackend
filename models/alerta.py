from db import db
from datetime import datetime
from models.alumno import Alumno
from models.historial import Historial

TIPOS_ALERTA = [
    ("RENDIMIENTO", "RENDIMIENTO"),
    ("OBSERVACION", "OBSERVACION"),
    ("ASISTENCIA", "ASISTENCIA"),
    ]

class Alerta(db.Document):
    tipo = db.StringField(choices=TIPOS_ALERTA)
    alumno = db.ReferenceField(Alumno)
    data = db.StringField(max_length=100)
    fecha = db.DateTimeField(default=datetime.now)
    historial = db.ListField(db.EmbeddedDocumentField(Historial))