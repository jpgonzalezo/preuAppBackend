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
    nombre_usuario = db.StringField(max_length=20)
    password = db.StringField(max_length=12)
    direccion = db.EmbeddedDocumentField(Direccion)
    rut = db.StringField(max_length=10)
    alumno = db.ReferenceField(Alumno)
    meta = {'strict': False}

    def __str__(self):
        return self.nombres