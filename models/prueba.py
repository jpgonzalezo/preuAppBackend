from db import db
from datetime import datetime
from models.alumno import Alumno
from models.curso import Curso
from models.respuesta import Respuesta
from models.pregunta import Pregunta
from models.asignatura import Asignatura
from models.topico import Topico
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
    topicos = db.ListField(db.ReferenceField(Topico))
    tipo = db.StringField(choices=TIPOS_PRUEBA)
    activo = db.BooleanField(default=True)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre
    
    def to_dict(self):
        topicos = []
        for topico in self.topicos:
            topicos.append(topico.to_dict())
        preguntas = []
        for pregunta in self.preguntas:
            preguntas.append(pregunta.to_dict())
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "cantidad_preguntas": self.cantidad_preguntas,
            "asignatura": self.asignatura.to_dict(),
            "fecha": str(self.fecha),
            "tipo": self.tipo,
            "topicos": topicos,
            "preguntas": preguntas
        }