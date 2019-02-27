from db import db

class Region(db.Document):
    nombre = db.StringField()
    meta = {'strict': False}
    def __str__(self):
        return self.nombre