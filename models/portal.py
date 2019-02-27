from db import db
from models.institucion import Institucion
from models.seccion import Seccion

class Portal(db.Document):
    titulo = db.StringField(max_length=50)
    logo = db.ImageField()
    institucion = db.ReferenceField(Institucion)
    db.ListField(db.EmbeddedDocumentField(Seccion))