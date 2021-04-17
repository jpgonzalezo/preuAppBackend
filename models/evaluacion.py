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

    #TODO: validar si existen los objetos asociados
    @classmethod
    def evaluar_prueba(cls, alumno_id, body):
        prueba_id = body["prueba_id"]
        listado_respuestas = body["respuestas"]
        prueba = Prueba.objects(id=prueba_id).first()
        alumno = Alumno.objects(id=alumno_id).first()

        evaluacion = Evaluacion()
        cantidad_buenas = 0
        cantidad_malas = 0
        cantidad_omitidas = 0
        evaluacion.alumno = alumno
        evaluacion.prueba = prueba
        for pregunta in prueba.preguntas:
            respuesta = Respuesta()
            respuesta.numero_pregunta = pregunta.numero_pregunta
            if listado_respuestas[str(pregunta.numero_pregunta)] == "":
                cantidad_omitidas = cantidad_omitidas + 1
                respuesta.correcta = False
                if prueba.tipo != "TAREA":
                    respuesta.alternativa = "O"
            else:
                if prueba.tipo != "TAREA":
                    if listado_respuestas[str(pregunta.numero_pregunta)].upper() == pregunta.alternativa.upper():
                        cantidad_buenas = cantidad_buenas + 1
                        respuesta.correcta = True
                    else:
                        cantidad_malas = cantidad_malas + 1
                        respuesta.correcta = False
                    respuesta.alternativa = str(listado_respuestas[str(pregunta.numero_pregunta)].upper())
                else:
                    if listado_respuestas[str(pregunta.numero_pregunta)].upper() == "CORRECTA":
                        cantidad_buenas = cantidad_buenas + 1
                        respuesta.correcta = True
                    if listado_respuestas[str(pregunta.numero_pregunta)].upper() == "INCORRECTA":
                        cantidad_malas = cantidad_malas + 1
                        respuesta.correcta = False
            evaluacion.respuestas.append(respuesta)
        evaluacion.cantidad_buenas = cantidad_buenas
        evaluacion.cantidad_malas = cantidad_malas
        evaluacion.cantidad_omitidas = cantidad_omitidas
        evaluacion.puntaje = int(((850 - prueba.puntaje_base)/len(prueba.preguntas))*cantidad_buenas + prueba.puntaje_base)
        evaluacion.save()
        return {'Response':'exito'}
   