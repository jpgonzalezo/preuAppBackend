from flask import Flask, Blueprint, jsonify, request
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.administrador import Administrador
from models.profesor import Profesor
from models.alumno import Alumno
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from flask_restful import reqparse
from utils.trata_contrasena import created_random_pass_by_profile as change_passCodigo
from utils.trata_contrasena import validate_code_provisional, change_pass



import json

def init_module(api):
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(CambiarContrasena, '/cambiar_contrasena')
    api.add_resource(CodigoRecuperacion, '/codigo_recuperacion')
    api.add_resource(CambiaContrasenaCodigo, '/olvide_contrasena')


class Login(Resource):
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        if(data['tipo'] == 'ADMINISTRADOR'):
            administrador = Administrador.objects(email = data['email']).first()
            if(administrador == None):
                return {'respuesta': 'no_existe'}
            else:
                if administrador.check_password(data['password']):
                    token = administrador.get_token()
                    return {'tipo': 'ADMINISTRADOR','token': str(token)}
                else:
                    return {'respuesta': 'no_existe'}

        if(data['tipo'] == 'PROFESOR'):
            profesor = Profesor.objects(email = data['email']).first()
            if(profesor == None):
                return {'respuesta': 'no_existe'}
            else:
                if profesor.check_password(data['password']):
                    token = profesor.get_token()
                    return {'tipo': 'PROFESOR','token': str(token)}
                else:
                    return {'respuesta': 'no_existe'}
        
        if(data['tipo'] == 'ALUMNO'):
            alumno = Alumno.objects(email = data['email']).first()
            if(alumno == None):
                return {'respuesta': 'no_existe'}
            else:
                if alumno.check_password(data['password']):
                    token = alumno.get_token()
                    return {'tipo': 'ALUMNO','token': str(token)}
                else:
                    return {'respuesta': 'no_existe'}

        if(data['tipo'] == 'APODERADO'):
            apoderado = Apoderado.objects(email = data['email']).first()
            if(apoderado == None):
                return {'respuesta': 'no_existe'}
            else:
                if apoderado.check_password(data['password']):
                    token = apoderado.get_token()
                    return {'tipo': 'APODERADO','token': str(token)}
                else:
                    return {'respuesta': 'no_existe'}
class Logout(Resource):
    def post(self):
        return {'respuesta': True}

class CodigoRecuperacion(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(CodigoRecuperacion, self).__init__()
    
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        user_mail = data['email']
        admin = Administrador.get_by_email_or_username(user_mail)
        alumno = Alumno.get_by_email_or_username(user_mail)
        apoderado = Apoderado.get_by_email_or_username(user_mail)
        profesor = Profesor.get_by_email_or_username(user_mail)
        result = change_passCodigo(user_mail,admin,alumno,apoderado,profesor)
        if (result == False):
            return 'usuario no registrado.', 404
        else: 
            return 'correo enviado correctamente a email indicado.', 200

class CambiaContrasenaCodigo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(CambiaContrasenaCodigo, self).__init__()
    
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        user_mail = data['email']
        user_codigo = data['codigo']
        user_new_pass = data['new_pass']
        admin = Administrador.get_by_email_or_username(user_mail)
        alumno = Alumno.get_by_email_or_username(user_mail)
        apoderado = Apoderado.get_by_email_or_username(user_mail)
        profesor = Profesor.get_by_email_or_username(user_mail)
        if ( alumno != None or admin != None or apoderado != None or profesor != None):
            lista = validate_code_provisional(admin,alumno,apoderado,profesor)
            list_codes = lista[1]
            count_profile = lista[0]
            count_equals_code = list_codes.count(user_codigo)
            if count_profile == count_equals_code:
                return change_pass(user_new_pass, admin, alumno, apoderado, profesor), 200
            else: 
                return 'Código ingresado invalido', 404

        else:
            return "Usuario no encontrado", 404
        #return change_pass(user_mail,admin,alumno,apoderado,profesor)


class CambiarContrasena(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(CambiarContrasena, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        
        #trabajar directamente con el usuario que cambia contraseña
        user = None
        if alumno != None:
            user = alumno 
        elif apoderado != None:
            user = apoderado
        elif administrador != None:
            user = administrador
        elif profesor != None:
            user = profesor
        if user ==None:
            return {'message':'invalid_user'}
        #Obtener los campos del formulario de cambio de contraseña
        data = request.data.decode()
        data = json.loads(data)

        #Validar que la contraseña actual sea valida
        if user.check_password(data['actual_password']):
            #Cambiar contraseña
            user.encrypt_password(data['new_password'])
            user.save()
            return {'message':'great'}
        else:
            return {"message":"incorrect_password"}
