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
    nombre_usuario = db.StringField(max_length=20)
    password = db.StringField(max_length=12)
    direccion = db.EmbeddedDocumentField(Direccion)
    rut = db.StringField(max_length=10)
    asignatura = db.ReferenceField(Asignatura)
    meta = {'strict': False}