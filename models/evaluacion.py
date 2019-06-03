from db import db
from datetime import datetime
from models.alumno import Alumno
from models.respuesta import Respuesta
from models.prueba import Prueba
from models.asignatura import Asignatura
import mongoengine_goodjson as gj

class Evaluacion(gj.Document):
    alumno = db.ReferenceField(Alumno)
    prueba = db.ReferenceField(Prueba)
    cantidad_buenas = db.IntField()
    cantidad_malas = db.IntField()
    cantidad_omitidas = db.IntField()
    puntaje = db.IntField()
    fecha = db.DateTimeField(default=datetime.now)
    respuestas = db.ListField(db.EmbeddedDocumentField(Respuesta))
    meta = {'strict': False}

    def to_dict(self):
        respuestas = []
        for respuesta in self.respuestas:
            respuestas.append(respuesta.to_dict())
        return{
            "id": str(self.id),
            "alumno": self.alumno.to_dict(),
            "prueba": self.prueba.to_dict(),
            "cantidad_buenas": self.cantidad_buenas,
            "cantidad_malas": self.cantidad_malas,
            "cantidad_omitidas": self.cantidad_omitidas,
            "puntaje": self.puntaje,
            "fecha": str(self.fecha),
            "respuestas": respuestas
        }