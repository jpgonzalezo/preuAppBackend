from db import db
from datetime import datetime
from models.direccion import Direccion

class Colegio(db.Document):
    nombre = db.StringField(verbose_name="Nombre Institucion", max_length=200)
    direccion = db.EmbeddedDocumentField(Direccion)

    meta = {'strict': False}

    def __str__(self):
        return self.nombre