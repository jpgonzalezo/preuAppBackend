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
        headers = ["Numero", "Alternativa Correcta", "Id. Topico"]
        result_list = [Topico.export_to_excel(asignatura_id)]
        return create_excel(result_list, headers, "Formato_preguntas")

    # TODO: validar id del topico y q venga la alternativa entre los valores permitidos
    @classmethod
    def create_from_excel(cls, list_rows):
        list_preguntas = []
        for index, pregunta in enumerate(list_rows):
            try:
                topico = Topico.objects(id=pregunta[2]).first()
                if(topico == None):
                    return []
            except:
                return []
            if( pregunta[1] == "None" or not(pregunta[1] in ["A","B","C","D","E"])):
                return []
            alternativa = pregunta[1]
            preguntaNuevo = Pregunta(numero_pregunta = index+1,
                                     alternativa = alternativa,
                                     topico = topico)
            list_preguntas.append(preguntaNuevo)
        return list_preguntas
