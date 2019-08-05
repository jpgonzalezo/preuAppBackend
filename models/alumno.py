from db import db
from datetime import datetime
from models.direccion import Direccion
from models.colegio import Colegio
from models.curso import Curso
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import mongoengine_goodjson as gj
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect,
    url_for,
    current_app,
    abort,
    Response,
    jsonify
    )

TIPOS_SEXOS = [
    ("MASCULINO", "MASCULINO"),
    ("FEMENINO", "FEMENINO"),
    ("NO DEFINIDO", "NO DEFINIDO"),
    ]

class Alumno(gj.Document):
    nombres = db.StringField()
    apellido_paterno = db.StringField(max_length=20)
    apellido_materno = db.StringField(max_length=20)
    email = db.EmailField()
    telefono = db.StringField()
    password = db.StringField(max_length=12)
    direccion = db.EmbeddedDocumentField(Direccion)
    colegio = db.ReferenceField(Colegio)
    rut = db.StringField()
    sexo = db.StringField(choices=TIPOS_SEXOS)
    puntaje_ingreso = db.IntField()
    curso = db.ReferenceField(Curso)
    imagen = db.StringField()
    activo = db.BooleanField(default=True)
    meta = {'strict': False}

    def __str__(self):
        return self.nombres

    def to_dict(self):
        return{
            "id": str(self.id),
            "nombres": self.nombres,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "email": self.email,
            "telefono": self.telefono,
            "colegio": self.colegio.to_dict(),
            "direccion": self.direccion.to_dict(),
            "sexo": self.sexo,
            "puntaje_ingreso": self.puntaje_ingreso,
            "curso": self.curso.to_dict(),
            "rut": self.rut,
            "imagen": self.imagen
        }
    
    def encrypt_password(self, password_to_encrypt):
    	self.password = generate_password_hash(password_to_encrypt)

    def check_password(self, password_to_check):
        print(check_password_hash(self.password, str(password_to_check)))
        return check_password_hash(self.password, str(password_to_check))
    @classmethod
    def get_by_email_or_username(cls, email_or_usernmane):
        text_id = email_or_usernmane.lower()
        if '@' in text_id:
            return cls.objects.filter(email=text_id).first()
        return cls.objects.filter(username=text_id).first()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.objects(id=user_id).first()
    # token alive 10 hours
    def get_token(self, seconds_live=36000):
        token = Serializer(current_app.config.get("TOKEN_KEY"),
                           expires_in=seconds_live)
        return str(token.dumps({'id': str(self.id)}))

    @classmethod
    def load_from_token(cls, token):
        s = Serializer(current_app.config.get("TOKEN_KEY"))
        if token[0:2] == "b'" and token[-1:] == "'":
            token = token[2:-1]
        try:
            data = s.loads(token)
            return cls.get_by_id(data['id'])
        except SignatureExpired:
            # the token has ben expired
            return None
        except BadSignature:
            # the token ist'n valid
            return None
        return None