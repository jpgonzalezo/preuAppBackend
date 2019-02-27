from db import db
from datetime import datetime
from models.alternativa import Alternativa

TIPOS_PREGUNTA = [
    ("SELECCION_MULTIPLE", "SELECCION_MULTIPLE"),
    ("VERDADERO_FALSO", "VERDADERO_FALSO"),
    ("ALTERNATIVA", "ALTERNATIVA"),
    ]
class Pregunta(db.EmbeddedDocument):
    texto = db.StringField()
    correcta = db.BooleanField(default=False)
    tipo_pregunta = db.StringField(choices=TIPOS_PREGUNTA)
    alternativas = db.ListField(db.EmbeddedDocumentField(Alternativa))
    meta = {'strict': False}