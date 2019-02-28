from db import db
from datetime import datetime

class Asignatura(db.Document):
    nombre = db.StringField(verbose_name="Nombre Asignatura", max_length=200)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre