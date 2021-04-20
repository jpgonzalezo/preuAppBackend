from flask import Flask, Blueprint, jsonify, request
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.administrador import Administrador
from models.profesor import Profesor
from models.alumno import Alumno
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from flask_restful import reqparse
import json

def init_module(api):
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(CambiarContrasena, '/cambiar_contrasena')


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
