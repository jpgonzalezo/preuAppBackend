from flask import Flask, Blueprint, jsonify, request
from models.anotacion import Anotacion
from models.alumno import Alumno
from models.profesor import Profesor
from models.administrador import Administrador
from models.apoderado import Apoderado
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from flask_restful import reqparse
def init_module(api):
    api.add_resource(AnotacionItem, '/anotaciones/<id>')
    api.add_resource(Anotaciones, '/anotaciones')
    api.add_resource(AnotacionesProfesor, '/anotaciones_profesor/<id>')


class AnotacionItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AnotacionItem, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return Anotacion.objects(id=id).first().to_dict()

class AnotacionesProfesor(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AnotacionesProfesor, self).__init__()
    def get(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        response = []
        profesor = Profesor.objects(id=id).first()
        for anotacion in Anotacion.objects(profesor=profesor.id).all():
            response.append(anotacion.to_dict())
        return response

class Anotaciones(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(Anotaciones, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        response = []
        for anotacion in Anotacion.objects().all():
            response.append(anotacion.to_dict())
        return response