from db import db
import mongoengine_goodjson as gj
class Administrador(gj.Document):
    nombres = db.StringField()
    apellido_paterno = db.StringField(max_length=20)
    apellido_materno = db.StringField(max_length=20)
    email = db.EmailField()
    telefono = db.StringField(max_length=12)
    nombre_usuario = db.StringField(max_length=20)
    password = db.StringField(max_length=12)
    meta = {'strict': False}

    def to_dict(self):
        return{
            "id": str(self.id),
            "nombres": self.nombre,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "email": self.email,
            "telefono": self.telefono,
            "nombre_usuario": self.nombre_usuario,
            "password": self.password
        }