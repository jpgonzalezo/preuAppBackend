from db import db
from datetime import datetime
from models.alumno import Alumno
from models.curso import Curso
from models.respuesta import Respuesta
from models.pregunta import Pregunta
from models.asignatura import Asignatura

TIPOS_PRUEBA = [
    ("ENSAYO", "ENSAYO"),
    ("TALLER", "TALLER"),
    ("TAREA", "TAREA"),
    ]
class Prueba(db.Document):
    nombre = db.StringField(max_length=50)
    cantidad_preguntas = db.IntField()
    asignatura = db.ReferenceField(Asignatura)
    fecha = db.DateTimeField(default=datetime.now)
    preguntas = db.ListField(db.EmbeddedDocumentField(Pregunta))
    tipo = db.StringField(choices=TIPOS_PRUEBA)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre