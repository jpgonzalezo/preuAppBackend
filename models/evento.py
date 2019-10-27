from db import db
from datetime import datetime
from models.curso import Curso
import mongoengine_goodjson as gj

class Evento(gj.Document):
    title = db.StringField(max_length=256)
    start = db.DateTimeField()
    backgroundColor = db.StringField()
    textColor = db.StringField(default="white")
    cursos = db.ListField(db.ReferenceField(Curso))
    activo = db.BooleanField(default=False)
    eliminado = db.BooleanField(default=True)

    def setStart(self):
        mes = str(self.start.month)
        dia = str(self.start.day)
        if len(str(self.start.month)) is 1:
            mes = "0"+str(self.start.month)
        if len(str(self.start.day)) is 1:
            dia = "0"+str(self.start.day)
        return str(self.start.year)+"-"+mes+"-"+dia

    def to_dict(self):
        return{
            "id": str(self.id),
            "title": self.title,
            "start": self.setStart(),
            "backgroundColor": self.backgroundColor,
            "textColor": self.textColor
        }