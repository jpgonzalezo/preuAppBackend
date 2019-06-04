from flask import Flask, Blueprint, jsonify, request
from models.evento import Evento
from models.curso import Curso
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from datetime import datetime
import json
from bson import json_util

def init_module(api):
    api.add_resource(EventoItem, '/eventos/<id>')
    api.add_resource(Eventos, '/eventos')
    api.add_resource(EventosSolicitudes, '/eventos/solicitudes')

class EventoItem(Resource):
    def get(self, id):
        return json.loads(Colegio.objects(id=id).first().to_json())
    
    def delete(self,id):
        evento = Evento.objects(id=id).first()
        evento.delete()
        return {'Response':'exito'}
    
    def put(self,id):
        evento = Evento.objects(id=id).first()
        evento.activo = True
        evento.save()
        return {'Response':'exito'}


class Eventos(Resource):
    def get(self):
        response = []
        eventos = Evento.objects().all()
        for evento in eventos:
            if evento.activo:
                response.append(evento.to_dict())
        return response
    
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        evento = Evento()
        evento.title = data['title']
        evento.backgroundColor = data['backgroundColor']
        curso = Curso.objects(id=data['curso']).first()
        evento.curso = curso.id
        evento.start = datetime.strptime(data['fecha'], '%Y-%m-%d')
        evento.save()
        return {'Response':'exito'}

class EventosSolicitudes(Resource):
    def get(self):
        response = []
        eventos = Evento.objects().all()
        for evento in eventos:
            if evento.activo is False:
                response.append(evento.to_dict())
        return response