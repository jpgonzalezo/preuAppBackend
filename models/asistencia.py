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
        alumnos_presentes = []
        alumnos_ausentes = []
        for alumno in self.alumnos_presentes:
            alumno_aux = Alumno.objects(id=alumno.id).first()
            alumnos_presentes.append(alumno_aux.to_dict())

        for alumno in self.alumnos_ausentes:
            alumno_aux = Alumno.objects(id=alumno.id).first()
            alumnos_ausentes.append(alumno_aux.to_dict())

        return{
            "id": str(self.id),
            "asignatura" : asignatura.to_dict(),
            "alumnos_presentes" : alumnos_presentes,
            "alumnos_ausentes" : alumnos_ausentes
        }