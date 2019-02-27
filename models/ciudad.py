from db import db
from models.region import Region
class Ciudad(db.Document):
    nombre = db.StringField()
    region = db.ReferenceField(Region)
    meta = {'strict': False}
    def __str__(self):
        return self.nombre