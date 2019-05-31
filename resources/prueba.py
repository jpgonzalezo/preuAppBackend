from flask import Flask, Blueprint, jsonify, request
from models.prueba import Prueba
from models.asignatura import Asignatura
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(PruebaItem, '/pruebas/<id>')
    api.add_resource(Pruebas, '/pruebas')
    api.add_resource(PruebasAsignatura, '/pruebas_asignatura/<id>')

class PruebasAsignatura(Resource):
    def get(self,id):
        response = []
        asignatura = Asignatura.objects(id=id).first()
        for prueba in Prueba.objects(asignatura=asignatura.id):
            response.append(prueba.to_dict())
        return response
class PruebaItem(Resource):
    def get(self, id):
        return json.loads(Prueba.objects(id=id).first().to_json())

class Pruebas(Resource):
    def get(self):
        response = []
        pruebas = Prueba.objects().all()
        for prueba in pruebas:
            if prueba.activo:
                response.append(prueba.to_dict())
        return response