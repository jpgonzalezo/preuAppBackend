from flask import Flask, Blueprint, jsonify, request
from models.anotacion import Anotacion
from models.alumno import Alumno
from models.profesor import Profesor 
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(AnotacionItem, '/anotaciones/<id>')
    api.add_resource(Anotaciones, '/anotaciones')
    api.add_resource(AnotacionesProfesor, '/anotaciones_profesor/<id>')


class AnotacionItem(Resource):
    def get(self, id):
        return Anotacion.objects(id=id).first().to_dict()

class AnotacionesProfesor(Resource):
    def get(self,id):
        response = []
        profesor = Profesor.objects(id=id).first()
        for anotacion in Anotacion.objects(profesor=profesor.id).all():
            response.append(anotacion.to_dict())
        return response

class Anotaciones(Resource):
    def get(self):
        response = []
        for anotacion in Anotacion.objects().all():
            response.append(anotacion.to_dict())
        return response