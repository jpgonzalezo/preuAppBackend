from db import db
from datetime import datetime

class Institucion(db.Document):
    nombre = db.StringField(verbose_name="Nombre Institucion", max_length=200)
    fecha_creacion = db.DateTimeField(default=datetime.now)

    meta = {'strict': False}

    def __str__(self):
        return self.nombre