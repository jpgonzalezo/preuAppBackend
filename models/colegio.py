from db import db
from datetime import datetime
from models.direccion import Direccion
import mongoengine_goodjson as gj

class Colegio(gj.Document):
    nombre = db.StringField(verbose_name="Nombre Institucion", max_length=200)
    direccion = db.EmbeddedDocumentField(Direccion)
    activo = db.BooleanField(default=True)
    cantidad_estudiantes = db.IntField(default=0)

    meta = {'strict': False}

    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "cantidad_estudiantes": self.cantidad_estudiantes,
            "direccion": self.direccion.to_dict()
        }
    
    def __str__(self):
        return self.nombre
    
    def updateCantEstudiantes(self):
        from models.alumno import Alumno
        alumnos = Alumno.objects(colegio=self).all()
        contador = 0
        for alumno in alumnos:
            if alumno.activo:
                contador= contador+1
        self.cantidad_estudiantes = contador
        return True
