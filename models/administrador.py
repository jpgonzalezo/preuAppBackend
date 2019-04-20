from db import db
import mongoengine_goodjson as gj
class Administrador(gj.Document):
    nombres = db.StringField()
    rut = db.StringField()
    apellido_paterno = db.StringField(max_length=20)
    apellido_materno = db.StringField(max_length=20)
    email = db.EmailField()
    telefono = db.StringField(max_length=12)
    password = db.StringField(max_length=12)
    activo = db.BooleanField(default=True)
    imagen = db.StringField()
    meta = {'strict': False}

    def to_dict(self):
        return{
            "id": str(self.id),
            "nombres": self.nombres,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "email": self.email,
            "telefono": self.telefono,
            "rut": self.rut,
            "imagen": self.imagen
        }