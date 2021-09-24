from db import db
from datetime import datetime
from models.profesor import Profesor
from models.alumno import Alumno
import mongoengine_goodjson as gj

class Anotacion(gj.Document):
    titulo = db.StringField(max_length=30)
    contenido = db.StringField(max_length=300)
    profesor = db.ReferenceField(Profesor)
    alumno = db.ReferenceField(Alumno)
    fecha = db.DateTimeField(default=datetime.now)

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "contenido": self.contenido,
            "profesor": self.profesor.to_dict(),
            "alumno": self.alumno.to_dict(),
            "fecha": self.fecha.strftime("%Y/%m/%d %H:%M:%S")
        }