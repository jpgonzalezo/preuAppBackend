from db import db
from datetime import datetime
from models.alumno import Alumno
from models.historial import Historial
from models.asignatura import Asignatura 
TIPOS_ALERTA = [
    ("RENDIMIENTO", "RENDIMIENTO"),
    ("ASISTENCIA", "ASISTENCIA"),
    ]

class Alerta(db.Document):
    tipo = db.StringField(choices=TIPOS_ALERTA)
    alumno = db.ReferenceField(Alumno)
    asignatura = db.ReferenceField(Asignatura)
    data = db.StringField(max_length=250)
    fecha = db.DateTimeField(default=datetime.now)
    historial = db.ListField(db.EmbeddedDocumentField(Historial))

    def getFecha(self):
        mes = str(self.fecha.month)
        dia = str(self.fecha.day)
        if len(str(self.fecha.month)) is 1:
            mes = "0"+str(self.fecha.month)
        if len(str(self.fecha.day)) is 1:
            dia = "0"+str(self.fecha.day)
        return str(self.fecha.year)+"-"+mes+"-"+dia+" "+str(self.fecha.hour)+":"+str(self.fecha.minute)+":"+str(self.fecha.second)

    def to_dict(self):
        return {
            "id": str(self.id),
            "alumno": self.alumno.to_dict(),
            "data": self.data,
            "fecha": self.getFecha(),
            "tipo": self.tipo,
            "asignatura": self.asignatura.to_dict()
        }