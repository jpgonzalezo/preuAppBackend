from db import db
from datetime import datetime
from models.pregunta import Pregunta

class Respuesta(db.EmbeddedDocument):
    data = db.StringField()
    meta = {'strict': False}