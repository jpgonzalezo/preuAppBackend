from flask import Flask, Blueprint, jsonify, request
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.administrador import Administrador
from models.profesor import Profesor
from models.alumno import Alumno
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')


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