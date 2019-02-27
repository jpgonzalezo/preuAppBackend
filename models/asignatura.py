from db import db
from datetime import datetime
from models.institucion import Institucion

class Asignatura(db.Document):
    nombre = db.StringField(verbose_name="Nombre Asignatura", max_length=200)
    institucion = db.ReferenceField(Institucion)

    meta = {'strict': False}

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
                "nombre": self.nombre,
                "institucion": self.institucion.nombre}