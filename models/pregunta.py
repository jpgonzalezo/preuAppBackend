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
    def create_layout_excel(cls):
        headers = ["Numero","Alternativa Correcta", "Id. Topico"]
        result_list = [Topico.export_to_excel()]
        return create_excel(result_list, headers, "Formato_preguntas")