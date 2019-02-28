from db import db
from datetime import datetime
from models.alumno import Alumno
from models.asistencia import Asistencia

class Justificacion(db.Document):
    fecha = db.DateTimeField(default=datetime.now)
    asistencia = db.ReferenceField(Asistencia)
    alumno = db.ReferenceField(Alumno)
    causa = db.StringField(max_length=200)