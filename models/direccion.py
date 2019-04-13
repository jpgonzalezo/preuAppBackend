from db import db
from models.region import Region
from models.ciudad import Ciudad
from models.comuna import Comuna

class Direccion(db.EmbeddedDocument):
    calle = db.StringField(max_length=50)
    numero = db.StringField(max_length=50)
    comuna = db.StringField(max_length=50)
    meta = {'strict': False}
    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
            "id": str(self.id),
            "calle": self.calle,
            "numero": self.numero,
            "comuna": self.comuna
        }