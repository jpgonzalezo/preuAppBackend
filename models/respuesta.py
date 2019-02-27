from db import db
from datetime import datetime

class Respuesta(db.EmbeddedDocument):
    data = db.StringField()
    correcta = db.BooleanField(default=False)
    meta = {'strict': False}