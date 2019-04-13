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

  def to_dict(self):
        curso = Curso.objects(id=self.curso.id).first()
        asignatura = Asignatura.objects(id=self.asignatura.id).first()
        alumnos_presentes = Alumno.objects(id=self.alumnos_presentes.id).first()
        alumnos_ausentes = Alumno.objects(id=self.alumnos_ausentes.id).first()
        return{
            "id": str(self.id)
            "curso" = curso.to_dict(),
            "asignatura" = asignatura.to_dict(),
            "alumnos_presentes" = alumnos_presentes.to_dict(),
            "alumnos_ausentes" = alumnos_ausentes.to_dict()
        }