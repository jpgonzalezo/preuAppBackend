from db import db
from models.ciudad import Ciudad
class Comuna(db.Document):
    nombre = db.StringField()
    ciudad = db.ReferenceField(Ciudad)
    meta = {'strict': False}
    def __str__(self):
        return self.nombre