from db import db
from datetime import datetime
from models.pregunta import Pregunta

ALTERNATIVAS = [
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
    ]
class Respuesta(db.EmbeddedDocument):
    correcta = db.BooleanField()
    numero_pregunta = db.IntField()
    alternativa = db.StringField(choices=ALTERNATIVAS)
    meta = {'strict': False}

    def to_dict(self):
        return {
            "correcta": self.correcta,
            "numero_pregunta": self.numero_pregunta,
            "alternativa": self.alternativa
        }