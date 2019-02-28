from db import db
from datetime import datetime
from models.alumno import Alumno
from models.curso import Curso
from models.asignatura import Asignatura

class Asistencia(db.Document):
    fecha = db.DateTimeField(default=datetime.now)
    curso = db.ReferenceField(Curso)
    asignatura = db.ReferenceField(Asignatura)
    alumnos_presentes = db.ListField(db.ReferenceField(Alumno))
    alumnos_ausentes = db.ListField(db.ReferenceField(Alumno))