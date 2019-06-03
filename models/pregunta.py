from db import db
from datetime import datetime
from models.alternativa import Alternativa
from models.topico import Topico

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