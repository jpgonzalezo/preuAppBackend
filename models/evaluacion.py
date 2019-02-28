from db import db
from datetime import datetime
from models.alumno import Alumno
from models.respuesta import Respuesta
from models.prueba import Prueba

class Evaluacion(db.Document):
    alumno = db.ReferenceField(Alumno)
    prueba = db.ReferenceField(Prueba)
    cantidad_buenas = db.IntField()
    cantidad_malas = db.IntField()
    cantidad_omitidas = db.IntField()
    puntaje = db.IntField()
    fecha = db.DateTimeField(default=datetime.now)
    respuestas = db.ListField(db.EmbeddedDocumentField(Respuesta))
    meta = {'strict': False}