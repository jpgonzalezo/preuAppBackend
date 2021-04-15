from db import db
from models.asignatura import Asignatura
import mongoengine_goodjson as gj
class Topico(gj.Document):
    nombre = db.StringField(verbose_name="Nombre Topico", max_length=200)
    asignatura = db.ReferenceField(Asignatura)
    activo = db.BooleanField(default=True)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
            "id": str(self.id),
            "asignatura": self.asignatura.to_dict(),
            "nombre": self.nombre
        }
    
    def to_excel(self):
        return [str(self.id),self.nombre, self.asignatura.to_dict()["nombre"]]
    
    @classmethod
    def export_to_excel(cls, asignatura_id):
        topicos= Topico.objects(asignatura= asignatura_id).all()
        result_list_topicos=[["Id. Topico", "Nombre Topico", "Asignatura"]]
        for topico in topicos:
            result_list_topicos.append(topico.to_excel())
        return result_list_topicos