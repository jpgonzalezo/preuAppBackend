from db import db
from datetime import datetime
from models.direccion import Direccion
from models.colegio import Colegio
from models.apoderado import Apoderado

class Alumno(db.Document):
    nombres = db.StringField()
    apellido_paterno = db.StringField(max_length=20)
    apellido_materno = db.StringField(max_length=20)
    email = db.EmailField()
    telefono = db.StringField(max_length=12)
    nombre_usuario = db.StringField(max_length=20)
    password = db.StringField(max_length=12)
    direccion = db.EmbeddedDocumentField(Direccion)
    colegio = db.ReferenceField(Colegio)
    apoderado = db.ReferenceField(Apoderado)
    meta = {'strict': False}

    def __str__(self):
        return self.nombres