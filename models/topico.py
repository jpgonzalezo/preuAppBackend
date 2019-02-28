from db import db
from models.asignatura import Asignatura

class Topico(db.Document):
    nombre = db.StringField(verbose_name="Nombre Topico", max_length=200)
    asignatura = db.ReferenceField(Asignatura)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre