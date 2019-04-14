from db import db
from datetime import datetime
from models.direccion import Direccion
import mongoengine_goodjson as gj

class Colegio(gj.Document):
    nombre = db.StringField(verbose_name="Nombre Institucion", max_length=200)
    direccion = db.EmbeddedDocumentField(Direccion)

    meta = {'strict': False}

    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "direccion": self.direccion.to_dict()
        }
    
    def __str__(self):
        return self.nombre