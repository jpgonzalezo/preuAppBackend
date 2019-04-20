from db import db
from datetime import datetime
from models.direccion import Direccion
from models.alumno import Alumno
import mongoengine_goodjson as gj
class Apoderado(gj.Document):
    nombres = db.StringField()
    apellido_paterno = db.StringField(max_length=20)
    apellido_materno = db.StringField(max_length=20)
    email = db.EmailField()
    telefono = db.StringField(max_length=12)
    password = db.StringField(max_length=12)
    direccion = db.EmbeddedDocumentField(Direccion)
    rut = db.StringField(max_length=10)
    alumno = db.ReferenceField(Alumno)
    imagen = db.StringField()
    activo = db.BooleanField(default=True)
    meta = {'strict': False}

    def __str__(self):
        return self.nombres
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "nombres": self.nombres,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion.to_dict(),
            "rut": self.rut,
            "alumno": self.alumno.to_dict(),
            "imagen": self.imagen
        }