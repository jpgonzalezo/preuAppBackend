from db import db
from datetime import datetime
from models.profesor import Profesor
from models.alumno import Alumno
import mongoengine_goodjson as gj

TIPOS_OBSERVACION = [
    ("OBSERVACION_PROFESOR", "OBSERVACION_PROFESOR"),
    ("OBSERVACION_ADMINISTRADOR", "OBSERVACION_ADMINISTRADOR"),
    ("OBSERVACION_PSICOLOGO", "OBSERVACION_PSICOLOGO"),
    ("OBSERVACION_PSICOPEDAGOGO", "OBSERVACION_PSICOPEDAGOGO"),
    ]

ANONIMATO = [
    ("ANONIMO", "ANONIMO"),
    ("NO_ANONIMO", "NO_ANONIMO"),
]

class Observacion(gj.Document):
    titulo = db.StringField(max_length=30)
    contenido = db.StringField(max_length=200)
    tipo = db.StringField(choices=TIPOS_OBSERVACION)
    nombre_personal = db.StringField(max_length=30)
    alumno = db.ReferenceField(Alumno)
    fecha = db.DateTimeField(default=datetime.now)

class ObservacionProfesor(gj.Document):
    titulo = db.StringField(max_length=30)
    contenido = db.StringField(max_length=200)
    anonimo = db.StringField(choices=ANONIMATO)
    alumno = db.ReferenceField(Alumno)
    profesor = db.ReferenceField(Profesor)
    fecha = db.DateTimeField(default=datetime.now)

    def to_dict(self):
        return{
            "id": str(self.id),
            "titulo": self.titulo,
            "contenido": self.contenido,
            "anonimo": self.anonimo,
            "alumno": self.alumno.to_dict(),
            "profesor": self.profesor.to_dict(),
            "fecha": str(self.fecha)
        }