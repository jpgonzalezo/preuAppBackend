from db import db
from datetime import datetime
from models.alumno import Alumno
from models.curso import Curso
from models.respuesta import Respuesta
from models.pregunta import Pregunta
from models.asignatura import Asignatura
import mongoengine_goodjson as gj
TIPOS_PRUEBA = [
    ("ENSAYO", "ENSAYO"),
    ("TALLER", "TALLER"),
    ("TAREA", "TAREA"),
    ]
class Prueba(gj.Document):
    nombre = db.StringField(max_length=50)
    cantidad_preguntas = db.IntField()
    asignatura = db.ReferenceField(Asignatura)
    fecha = db.DateTimeField(default=datetime.now)
    preguntas = db.ListField(db.EmbeddedDocumentField(Pregunta))
    tipo = db.StringField(choices=TIPOS_PRUEBA)
    activo = db.BooleanField(default=True)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "cantidad_preguntas": self.cantidad_preguntas,
            "asignatura": self.asignatura.to_dict(),
            "fecha": str(self.fecha),
            "tipo": self.tipo,
        }