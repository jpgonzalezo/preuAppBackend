from flask import Flask, Blueprint, jsonify, request
from models.asignatura import Asignatura
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(AsignaturaItem, '/asignaturas/<id>')
    api.add_resource(Asignaturas, '/asignaturas')


class AsignaturaItem(Resource):
    def get(self, id):
        return json.loads(Asignatura.objects(id=id).first().to_json())
    
    def delete(self,id):
        asignatura = Asignatura.objects(id=id).first()
        asignatura.activo = False
        asignatura.save()
        return {'Response':'exito'}


class Asignaturas(Resource):
    def get(self):
        asignaturas = []
        for asignatura in Asignatura.objects().all():
            if asignatura.activo:
                asignaturas.append(asignatura.to_dict())
        return asignaturas

    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        asignatura = Asignatura()
        asignatura.nombre = data['nombre']
        asignatura.save()
        return {'Response': 'exito'}