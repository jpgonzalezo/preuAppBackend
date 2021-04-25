from db import db
from datetime import datetime
from models.alumno import Alumno
from models.asistencia import Asistencia

class Justificacion(db.Document):
    fecha = db.DateTimeField(default=datetime.now)
    asistencia = db.ReferenceField(Asistencia)
    alumno = db.ReferenceField(Alumno)
    causa = db.StringField(max_length=200)
    activo = db.BooleanField(default=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "asistencia": self.asistencia.to_dict_short(),
            "alumno": self.alumno.to_dict(),
            "causa": self.causa,
            "fecha": self.fecha.strftime("%m/%d/%Y %H:%M:%S")
        }