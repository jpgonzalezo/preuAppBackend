from flask import Flask, Blueprint, jsonify
from models.alumno import Alumno
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(AlumnosItem, '/alumnos/<id>')
    api.add_resource(Alumnos, '/alumnos')


class AlumnosItem(Resource):
    def get(self, id):
        return json.loads(Alumnos.objects(id=id).first().to_json())


class Alumnos(Resource):
    def get(self):
        return json.loads(Alumno.objects().all().to_json())