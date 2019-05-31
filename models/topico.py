from db import db
from models.asignatura import Asignatura

class Topico(db.Document):
    nombre = db.StringField(verbose_name="Nombre Topico", max_length=200)
    asignatura = db.ReferenceField(Asignatura)
    activo = db.BooleanField(default=True)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
            "id": str(id),
            "asignatura": self.asignatura.to_dict(),
            "nombre": self.nombre
        }