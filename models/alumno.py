from db import db
from datetime import datetime
from models.direccion import Direccion
from models.colegio import Colegio
from models.curso import Curso
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import mongoengine_goodjson as gj
from utils.excel_util import create_workbook as create_excel
from utils.excel_util import map_to_option
from utils.excel_util import export as write_error
from utils.validaciones import validar_rut, es_correo_valido
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
TIPOS_SEXOS_ARRAY = [
    "MASCULINO",
    "FEMENINO",
    "NO DEFINIDO"
]

class Alumno(gj.Document):
    nombres = db.StringField()
    apellido_paterno = db.StringField(max_length=20)
    apellido_materno = db.StringField(max_length=20)
    email = db.EmailField()
    telefono = db.StringField()
    password = db.StringField()
    password_provisoria = db.StringField(default="no disponible")
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

    def to_excel(self):
        return [self.rut, self.nombres, self.apellido_paterno, self.apellido_materno]

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

    @classmethod
    # TODO: validar que vengan los id foraneos, el rut y correo con formato correo
    def create_from_excel(cls, list_rows):
        error_list = [["RUN", "Nombres", "Apellido Paterno", "Apellido Materno", "Puntaje Ingreso", "Sexo",
                       "Email", "Telefono", "Calle", "Numero", "Comuna", "Villa/Depto", "Id. Curso", "Id. Colegio", "Error"]]
        for alumno in list_rows:
            alumno = list(alumno)
            rut = str(alumno[0])
            if(rut != "None" and validar_rut(rut)):
                try:
                    curso = Curso.objects(id=alumno[12]).first()
                    if(curso == None):
                        alumno.append("Curso no existe")
                        error_list.append(alumno)
                        continue
                except:
                    alumno.append("Id de curso no es valido")
                    error_list.append(alumno)
                    continue

                try:
                    colegio = Colegio.objects(id=alumno[13]).first()
                    if(colegio == None):
                        alumno.append("Colegio no existe")
                        error_list.append(alumno)
                        continue
                except:
                    alumno.append("Id de colegio no es valido")
                    error_list.append(alumno)
                    continue

                if( alumno[5] == "None" or not(alumno[5] in TIPOS_SEXOS_ARRAY)):
                    alumno.append("Sexo ingresado no es valido")
                    error_list.append(alumno)
                    continue
                if( alumno[6] == "None" or not(es_correo_valido(alumno[6]))):
                    alumno.append("Correo ingresado no es valido")
                    error_list.append(alumno)
                    continue

                direccion = Direccion(calle=alumno[8], numero=str(alumno[9]), comuna=alumno[10], cas_dep_of=alumno[11])
                alumnoNuevo = Alumno(rut=str(alumno[0]),
                                     password = cls.encrypt_password(str(alumno[0])),
                                     nombres=alumno[1],
                                     apellido_paterno=alumno[2],
                                     apellido_materno=alumno[3],
                                     sexo=alumno[5],
                                     email=alumno[6],
                                     telefono=str(alumno[7]),
                                     direccion=direccion,
                                     colegio=colegio,
                                     curso=curso,
                                     imagen="default")
                if (alumno[4] != None and alumno[4] != ""):
                    alumnoNuevo.puntaje_ingreso = alumno[4]
                else:
                    alumnoNuevo.puntaje_ingreso = 0
                alumnoNuevo.save()
            else:
                alumno.append("RUT invalido")
                error_list.append(alumno)
        if(len(error_list) > 1):
            return write_error(error_list, "errores")
        return "hecho"

    @classmethod
    def create_layout_excel(cls):
        headers = ["RUN", "Nombres", "Apellido Paterno", "Apellido Materno", "Puntaje Ingreso", "Sexo (MASCULINO/FEMENINO/NO DEFINIDO)",
                   "Email", "Telefono", "Calle", "Numero", "Comuna", "Villa/Depto", "Id. Curso", "Id. Colegio"]
        result_list = [Colegio.export_to_excel(), Curso.export_to_excel()]
        return create_excel(result_list, headers, "Formato_alumnos")

    @classmethod
    def export_to_excel(cls):
        alumnos = Alumno.objects().all()
        result_list_alumnos = [["RUN", "Nombres", "Apellido Paterno", "Apellido Materno"]]
        for alumno in alumnos:
            result_list_alumnos.append(alumno.to_excel())
        return result_list_alumnos
        
    @classmethod
    def create_provisional_pass(cls,user_mail, provisional_pass):
        admin = cls.get_by_email_or_username(user_mail)
        admin.password_provisoria = provisional_pass
        admin.save()
        return 'hecho'
