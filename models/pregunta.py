from db import db
from datetime import datetime
from models.alternativa import Alternativa
from models.topico import Topico
from utils.excel_util import create_workbook as create_excel

ALTERNATIVAS = [
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
    ]
class Pregunta(db.EmbeddedDocument):
    numero_pregunta = db.IntField()
    topico = db.ReferenceField(Topico)
    alternativa = db.StringField(choices=ALTERNATIVAS)
    meta = {'strict': False}

    def to_dict(self):
        return {
            "numero_pregunta": self.numero_pregunta,
            "topico": self.topico.to_dict(),
            "alternativa": self.alternativa
        }

    @classmethod
    def create_layout_excel(cls, asignatura_id):
        headers = ["Numero","Alternativa Correcta", "Id. Topico"]
        result_list = [Topico.export_to_excel(asignatura_id)]
        return create_excel(result_list, headers, "Formato_preguntas")

    @classmethod
    def create_from_excel(cls, list_rows, asignatura_id):
        list_preguntas = []
        for pregunta in list_rows:
            topico = Topico.objects(asignatura = asignatura_id).first()
            preguntaNuevo = Pregunta(numero_pregunta = pregunta[0],
                                    alternativa = pregunta[1],
                                    topico = topico)
            list_preguntas.append(preguntaNuevo)
        return list_preguntas