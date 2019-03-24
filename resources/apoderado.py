from flask import Flask, Blueprint, jsonify
from models.apoderado import Apoderado
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(ApoderadoItem, '/apoderado/<id>')
    api.add_resource(Apoderados, '/apoderados')


class ApoderadoItem(Resource):
    def get(self, id):
        return json.loads(Apoderado.objects(id=id).first().to_json())


class Apoderados(Resource):
    def get(self):
        return json.loads(Apoderado.objects().all().to_json())