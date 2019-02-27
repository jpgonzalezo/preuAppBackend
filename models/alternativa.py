from db import db
from datetime import datetime

class Alternativa(db.EmbeddedDocument):
    texto = db.StringField()
    correcta = db.BooleanField(default=False)
    meta = {'strict': False}