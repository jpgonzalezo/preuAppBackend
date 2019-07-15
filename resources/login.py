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
                print(data['password'])
                print(administrador.check_password(data['password']))
                if administrador.check_password(data['password']):
                    return {'tipo':'ADMINISTRADOR','respuesta': json.loads(administrador.to_json())}
                else:
                    return {'respuesta': 'no_existe'}

        if(data['tipo'] == 'PROFESOR'):
            profesor = Profesor.objects(email = data['email'], password = data['password']).first()
            if(profesor == None):
                return {'respuesta': 'no_existe'}
            else:
                return {'tipo':'PROFESOR','respuesta': json.loads(profesor.to_json())}
        
        if(data['tipo'] == 'ALUMNO'):
            alumno = Alumno.objects(email = data['email'], password = data['password']).first()
            if(alumno == None):
                return {'respuesta': 'no_existe'}
            else:
                return {'tipo':'ALUMNO','respuesta': json.loads(alumno.to_json())}

class Logout(Resource):
    def post(self):
        return {'respuesta': True}