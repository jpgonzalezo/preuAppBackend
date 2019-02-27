from db import db
from datetime import datetime

class Seccion(db.EmbeddedDocument):
    data = db.StringField()
    correcta = db.BooleanField(default=False)
    meta = {'strict': False}