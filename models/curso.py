from db import db
from datetime import datetime
 
import mongoengine_goodjson as gj

class Curso(gj.Document):
    nombre = db.StringField(verbose_name="Nombre curso", max_length=200)
    cantidad_estudiantes = db.IntField(default=0)
    activo = db.BooleanField(default=True)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "cantidad_estudiantes": self.cantidad_estudiantes
        }

    def updateCantEstudiantes(self):
        from models.alumno import Alumno
        alumnos = Alumno.objects(curso=self).all()
        contador = 0
        for alumno in alumnos:
            if alumno.activo:
                contador= contador+1
        self.cantidad_estudiantes = contador
        return True