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

    def getFecha(self):
        mes = str(self.fecha.month)
        dia = str(self.fecha.day)
        if len(str(self.fecha.month)) is 1:
            mes = "0"+str(self.fecha.month)
        if len(str(self.fecha.day)) is 1:
            dia = "0"+str(self.fecha.day)
        return str(self.fecha.year)+"-"+mes+"-"+dia+" "+str(self.fecha.hour)+":"+str(self.fecha.minute)+":"+str(self.fecha.second)

    def to_dict_short(self):
        return{
            "id": str(self.id),
            "asignatura" : self.asignatura.nombre,
            "alumnos_presentes" : len(self.alumnos_presentes),
            "alumnos_ausentes" : len(self.alumnos_ausentes),
            "curso": self.curso.nombre,
            "fecha": self.getFecha()
        }

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
            "alumnos_ausentes" : alumnos_ausentes,
            "curso": self.curso.to_dict(),
            "fecha": self.getFecha()
        }