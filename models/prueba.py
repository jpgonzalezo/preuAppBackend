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
    puntaje_base = db.IntField(default=0)
    meta = {'strict': False}

    def getFecha(self):
        mes = str(self.fecha.month)
        dia = str(self.fecha.day)
        if len(str(self.fecha.month)) is 1:
            mes = "0"+str(self.fecha.month)
        if len(str(self.fecha.day)) is 1:
            dia = "0"+str(self.fecha.day)
        return str(self.fecha.year)+"-"+mes+"-"+dia+" "+str(self.fecha.hour)+":"+str(self.fecha.minute)+":"+str(self.fecha.second)

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
            "fecha": self.getFecha(),
            "tipo": self.tipo,
            "topicos": topicos,
            "preguntas": preguntas,
            "puntaje_base": self.puntaje_base
        }

    #TODO: validar que id de la prueba
    @classmethod    
    def load_preguntas(cls, lista, prueba_id):
        prueba =  Prueba.objects(id=prueba_id).first()
        prueba.preguntas = Pregunta.create_from_excel(lista)
        prueba.cantidad_preguntas = len(lista)
        prueba.save()
        return "preguntas cargadas"