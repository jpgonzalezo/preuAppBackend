from db import db
from datetime import datetime

class Historial(db.EmbeddedDocument):
    fecha = db.DateTimeField(default=datetime.now)
    id_visto = db.StringField()
    meta = {'strict': False}