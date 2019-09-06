from flask import Flask, Blueprint, jsonify, request
from models.prueba import Prueba
from models.evaluacion import Evaluacion
from models.administrador import Administrador
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.profesor import Profesor
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from flask_restful import reqparse

def init_module(api):
    api.add_resource(EvaluacionesPrueba, '/evaluaciones/prueba/<id>')


class EvaluacionesPrueba(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(EvaluacionesPrueba, self).__init__()
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
        prueba = Prueba.objects(id=id).first()
        for evaluacion in Evaluacion.objects(prueba=prueba.id):
            response.append(evaluacion.to_dict())
        return response