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

    def to_excel(self):
        return [str(self.id),self.nombre]
    
    def __str__(self):
        return self.nombre
    
    def updateCantEstudiantes(self):
        from models.alumno import Alumno
        alumnos = Alumno.objects(colegio=self.id).all()
        contador = 0
        for alumno in alumnos:
            if alumno.activo:
                contador= contador+1
        self.cantidad_estudiantes = contador
        return True

    @classmethod
    def create_from_excel(cls, list_rows):
        for colegio in list_rows:
            direccion = Direccion(calle = colegio[1], numero = str(colegio[2]), comuna = colegio[3])
            colegio = Colegio(direccion = direccion, nombre= colegio[0])
            colegio.save()
        return "hecho"

    @classmethod
    def export_to_excel(cls):
        colegios= Colegio.objects().all()
        result_list_colegios=[["Id. Colegio", "Nombre Colegio"]]
        for colegio in colegios:
            result_list_colegios.append(colegio.to_excel())
        return result_list_colegios

