from db import db
from datetime import datetime
from models.direccion import Direccion
from models.colegio import Colegio
from models.curso import Curso
import mongoengine_goodjson as gj

TIPOS_SEXOS = [
    ("MASCULINO", "MASCULINO"),
    ("FEMENINO", "FEMENINO"),
    ("NO DEFINIDO", "NO DEFINIDO"),
    ]

class Alumno(gj.Document):
    nombres = db.StringField()
    apellido_paterno = db.StringField(max_length=20)
    apellido_materno = db.StringField(max_length=20)
    email = db.EmailField()
    telefono = db.StringField()
    password = db.StringField(max_length=12)
    direccion = db.EmbeddedDocumentField(Direccion)
    colegio = db.ReferenceField(Colegio)
    rut = db.StringField()
    sexo = db.StringField(choices=TIPOS_SEXOS)
    puntaje_ingreso = db.IntField()
    curso = db.ReferenceField(Curso)
    imagen = db.StringField()
    meta = {'strict': False}

    def __str__(self):
        return self.nombres

    def to_dict(self):
        return{
            "id": str(self.id),
            "nombres": self.nombres,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "email": self.email,
            "telefono": self.telefono,
            "password": self.password,
            "colegio": self.colegio.to_dict(),
            "direccion": self.direccion.to_dict(),
            "sexo": self.sexo,
            "puntaje_ingreso": self.puntaje_ingreso,
            "curso": self.curso.to_dict(),
            "rut": self.rut,
            "imagen": self.imagen
        }