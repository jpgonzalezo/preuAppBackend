from flask import Flask, Blueprint, jsonify
from models.colegio import Colegio
from models.direccion import Direccion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(ColegioItem, '/colegios/<id>')
    api.add_resource(Colegios, '/colegios')


class ColegioItem(Resource):
    def get(self, id):
        return json.loads(Colegio.objects(id=id).first().to_json())
    
    def delete(self,id):
        colegio = Colegio.objects(id=id).first()
        colegio.activo = False
        colegio.save()
        return {'Response':'exito'}


class Colegios(Resource):
    def get(self):
        response = []
        colegios = Colegio.objects().all()
        for colegio in colegios:
            if colegio.activo:
                response.append(colegio.to_dict())
        return response

    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        colegio = Colegio()
        colegio.nombre = data['nombre']
        direccion = Direccion()
        direccion.calle = data['calle']
        direccion.numero = data['numero']
        direccion.comuna = data['comuna']
        colegio.direccion = direccion
        colegio.save()
        return {'Response':'exito'}
