from db import db
class Historial(db.EmbeddedDocument):
    data = db.StringField()
    correcta = db.BooleanField(default=False)
    meta = {'strict': False}