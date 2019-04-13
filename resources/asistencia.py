from flask import Flask, Blueprint, jsonify
from models.asistencia import Asistencia
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(AsistenciaItem, '/asistencia/<id>')
    api.add_resource(Asistencias, '/asistencias')


class AsistenciaItem(Resource):
    def get(self, id):
        return json.loads(Asistencia.objects(id=id).first().to_json())


class Asistencias(Resource):
    def get(self):
        response = []
        for asistencia in Asistencia.objects().all():
            response.append(asistencia.to_dict())
        return response