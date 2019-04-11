from flask import Flask, Blueprint, jsonify, request
from models.observacion import Observacion
from models.alumno import Alumno
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(ObservacionItem, '/observacion/<id>')
    api.add_resource(Observaciones, '/observaciones')
    api.add_resource(ObservacionAlumno, '/observaciones_alumno/<id>/<tipo>')


class ObservacionItem(Resource):
    def get(self, id):
        return json.loads(Observacion.objects(id=id).first().to_json())

class ObservacionAlumno(Resource):
    def get(self,id,tipo):
        return json.loads(Observacion.objects(alumno=id,tipo=tipo).all().to_json())

class Observaciones(Resource):
    def get(self):
        return json.loads(Observacion.objects().all().to_json())
    
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        observacion = Observacion()
        observacion.titulo = data['titulo']
        observacion.contenido = data['contenido']
        observacion.tipo = data['tipo']
        observacion.nombre_personal = data['nombre_personal']
        observacion.alumno = Alumno.objects(id=data['alumno']).first()
        observacion.save()
        return {'Response': 'exito'}