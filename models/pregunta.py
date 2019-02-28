from db import db
from datetime import datetime
from models.alternativa import Alternativa
from models.topico import Topico

TIPOS_PREGUNTA = [
    ("TEXTO", "TEXTO"),
    ("ALTERNATIVA", "ALTERNATIVA"),
    ]
class Pregunta(db.EmbeddedDocument):
    texto = db.StringField()
    tipo_pregunta = db.StringField(choices=TIPOS_PREGUNTA)
    alternativas = db.ListField(db.EmbeddedDocumentField(Alternativa))
    topico = db.ReferenceField(Topico)
    meta = {'strict': False}