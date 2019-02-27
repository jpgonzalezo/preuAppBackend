from db import db
from datetime import datetime

class Profesor(db.Document):
    nombres = db.StringField(max_length=20)
    apellido_paterno = db.StringField(max_length=20)
    apellido_materno = db.StringField(max_length=20)
    email = db.EmailField()
    telefono = db.StringField(max_length=12)
    nombre_usuario = db.StringField(max_length=20)
    password = db.StringField(max_length=12)
    meta = {'strict': False}