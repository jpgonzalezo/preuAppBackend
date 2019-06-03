from flask import Flask, Blueprint, jsonify, request
from models.topico import Topico
from models.asignatura import Asignatura
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(TopicoItem, '/topicos/<id>')
    api.add_resource(Topicos, '/topicos')
    api.add_resource(TopicosAsignatura, '/topicos_asignatura/<id>')


class TopicoItem(Resource):
    def get(self, id):
        return Topico.objects(id=id).first().to_dict()
    def delete(self,id):
        topico = Topico.objects(id=id).first()
        topico.activo = False
        topico.save()
        return {"Response":"borrado"}
class TopicosAsignatura(Resource):
    def get(self,id):
        response = []
        asignatura = Asignatura.objects(id=id).first()
        for topico in Topico.objects(asignatura=asignatura.id).all():
            if topico.activo:
                response.append(topico.to_dict())
        return response

class Topicos(Resource):
    def get(self):
        response = []
        for topico in Topico.objects().all():
            if topico.activo:
                response.append(anotacion.to_dict())
        return response