from db import db
from datetime import datetime
from models.alumno import Alumno
 
import mongoengine_goodjson as gj
class Curso(gj.Document):
    nombre = db.StringField(verbose_name="Nombre curso", max_length=200)
    alumnos = db.ListField(db.ReferenceField(Alumno))
    meta = {'strict': False}