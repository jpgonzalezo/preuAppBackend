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
    visible = db.BooleanField(default=False) 
    activo = db.BooleanField(default=True)
    puntaje_base = db.IntField(default=0)
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
            "fecha": self.fecha.strftime("%Y/%m/%d %H:%M:%S"),
            "tipo": self.tipo,
            "topicos": topicos,
            "preguntas": preguntas,
            "puntaje_base": self.puntaje_base,
            "visible": self.visible
        }

    #TODO: validar que id de la prueba
    @classmethod    
    def load_preguntas(cls, lista, prueba_id):
        try:
            prueba =  Prueba.objects(id=prueba_id).first()
            if(prueba == None):
                return {"error":"Prueba no encontrada"}
        except:
            return {"error": "Error en el id de la prueba"}

        listado_preguntas = Pregunta.create_from_excel(lista)
        if(len(listado_preguntas) == 0):
            return {"error":"Problema al cargar las preguntas de la prueba, favor revisar excel"}
        prueba.preguntas = listado_preguntas
        prueba.cantidad_preguntas = len(lista)
        prueba.save()
        return {"Response":"Prueba creada con exito"}
    
    @classmethod
    def list_to_dict(cls,lista):
        result_list=[]
        for element in lista:
            result_list.append(element.to_dict())
        return result_list

    @classmethod
    def update_visible(cls, id_prueba):
        prueba = Prueba.objects(id = id_prueba).first()
        prueba.visible = not prueba.visible
        prueba.save()
        return "Campo visible actualizado"
