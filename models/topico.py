from db import db
from models.asignatura import Asignatura
import mongoengine_goodjson as gj
class Topico(gj.Document):
    nombre = db.StringField(verbose_name="Nombre Topico", max_length=200)
    asignatura = db.ReferenceField(Asignatura)
    activo = db.BooleanField(default=True)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
            "id": str(self.id),
            "asignatura": self.asignatura.to_dict(),
            "nombre": self.nombre
        }