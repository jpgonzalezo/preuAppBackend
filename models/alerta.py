from db import db
from datetime import datetime
from models.alumno import Alumno
from models.historial import Historial
from models.asignatura import Asignatura 
TIPOS_ALERTA = [
    ("RENDIMIENTO", "RENDIMIENTO"),
    ("ASISTENCIA", "ASISTENCIA"),
    ]

class Alerta(db.Document):
    tipo = db.StringField(choices=TIPOS_ALERTA)
    alumno = db.ReferenceField(Alumno)
    asignatura = db.ReferenceField(Asignatura)
    data = db.StringField(max_length=250)
    fecha = db.DateTimeField(default=datetime.now)
    historial = db.ListField(db.EmbeddedDocumentField(Historial))

    def to_dict(self):
        return {
            "id": str(self.id),
            "alumno": self.alumno.to_dict(),
            "data": self.data,
            "fecha": str(self.fecha),
            "tipo": self.tipo,
            "asignatura": self.asignatura.to_dict()
        }