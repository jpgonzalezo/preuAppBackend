from flask import Flask, Blueprint, jsonify
from models.curso import Curso
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(CursoItem, '/cursos/<id>')
    api.add_resource(Cursos, '/cursos')


class CursoItem(Resource):
    def get(self, id):
        return json.loads(Curso.objects(id=id).first().to_json())


class Cursos(Resource):
    def get(self):
        return json.loads(Curso.objects().all().to_json())