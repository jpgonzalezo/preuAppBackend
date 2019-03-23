from flask import Flask, Blueprint, jsonify
from models.colegio import Colegio
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


class Colegios(Resource):
    def get(self):
        return json.loads(Colegio.objects().all().to_json())