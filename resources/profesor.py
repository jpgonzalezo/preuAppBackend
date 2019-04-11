from flask import Flask, Blueprint, jsonify
from models.profesor import Profesor
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(ProfesorItem, '/profesores/<id>')
    api.add_resource(Profesores, '/profesores')


class ProfesorItem(Resource):
    def get(self, id):
        return json.loads(Profesor.objects(id=id).first().to_json())
    
    def delete(self, id):
        profesor = Profesor.objects(id=id).first()
        profesor.delete()
        return{'Response':'borrado'}

class Profesores(Resource):
    def get(self):
        return json.loads(Profesor.objects().all().to_json())