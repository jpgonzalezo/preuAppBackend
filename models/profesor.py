from db import db
from datetime import datetime
from models.asignatura import Asignatura
from models.direccion import Direccion
import mongoengine_goodjson as gj

class Profesor(gj.Document):
    nombres = db.StringField(max_length=20)
    apellido_paterno = db.StringField(max_length=20)
    apellido_materno = db.StringField(max_length=20)
    email = db.EmailField()
    telefono = db.StringField(max_length=12)
    password = db.StringField(max_length=12)
    direccion = db.EmbeddedDocumentField(Direccion)
    rut = db.StringField(max_length=10)
    asignatura = db.ReferenceField(Asignatura)
    imagen = db.StringField()
    activo = db.BooleanField(default=True)
    meta = {'strict': False}

    def to_dict(self):
        return {
            "id": str(self.id),
            "nombres": self.nombres,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "email": self.email,
            "telefono": self.telefono,
            "password": self.password,
            "direccion": self.direccion.to_dict(),
            "rut": self.rut,
            "asignatura": self.asignatura.to_dict(),
            "imagen": self.imagen
        }