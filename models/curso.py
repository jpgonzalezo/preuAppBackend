from db import db
from datetime import datetime
 
import mongoengine_goodjson as gj

class Curso(gj.Document):
    nombre = db.StringField(verbose_name="Nombre curso", max_length=200)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre
        }