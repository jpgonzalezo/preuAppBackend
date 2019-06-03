from flask import Flask, Blueprint, jsonify, request
from models.prueba import Prueba
from models.evaluacion import Evaluacion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(EvaluacionesPrueba, '/evaluaciones/prueba/<id>')

class EvaluacionesPrueba(Resource):
    def get(self,id):
        response = []
        prueba = Prueba.objects(id=id).first()
        for evaluacion in Evaluacion.objects(prueba=prueba.id):
            response.append(evaluacion.to_dict())
        return response