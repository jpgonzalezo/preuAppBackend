from flask import Flask, Blueprint, jsonify, request
from models.topico import Topico
from models.asignatura import Asignatura
from models.administrador import Administrador
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.profesor import Profesor
from models.prueba import Prueba
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from flask_restful import reqparse

def init_module(api):
    api.add_resource(TopicoItem, '/topicos/<id>')
    api.add_resource(TopicoPrueba, '/topicos/<id_topico>/prueba/<id_prueba>')
    api.add_resource(Topicos, '/topicos')
    api.add_resource(TopicosAsignatura, '/topicos_asignatura/<id>')
    api.add_resource(TopicosAsignaturaToken, '/topicos/asignatura')
    api.add_resource(TopicosPrueba, '/topicos/prueba/<id>')

class TopicoPrueba(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(TopicoPrueba, self).__init__()

    def delete(self,id_topico,id_prueba):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        if profesor == None:
            return {'response': 'user_invalid'},401
        prueba = Prueba.objects(id=id_prueba).first()
        topico = Topico.objects(id=id_topico).first()
        topicos = []
        for topico_prueba in prueba.topicos:
            if topico_prueba.id != topico.id:
                topicos.append(topico_prueba)
        prueba.topicos = topicos
        prueba.save()
        return {'Response':'borrado'}
        

class TopicosPrueba(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(TopicosPrueba, self).__init__()
    
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        if profesor == None:
            return {'response': 'user_invalid'},401
        return []

    
class TopicoItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(TopicoItem, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return Topico.objects(id=id).first().to_dict()
    def delete(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        topico = Topico.objects(id=id).first()
        topico.activo = False
        topico.save()
        return {"Response":"borrado"}

class TopicosAsignaturaToken(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(TopicosAsignaturaToken, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        response = []
        asignatura = Asignatura.objects(id=profesor.asignatura.id).first()
        for topico in Topico.objects(asignatura=asignatura.id).all():
            if topico.activo:
                response.append(topico.to_dict())
        return response

class TopicosAsignatura(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(TopicosAsignatura, self).__init__()
    def get(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        response = []
        asignatura = Asignatura.objects(id=id).first()
        for topico in Topico.objects(asignatura=asignatura.id).all():
            if topico.activo:
                response.append(topico.to_dict())
        return response

class Topicos(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(Topicos, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        response = []
        for topico in Topico.objects().all():
            if topico.activo:
                response.append(topico.to_dict())
        return response
    
    def post(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        if profesor == None:
            return {'response': 'user_invalid'},401
        data = request.data.decode()
        data = json.loads(data)
        topico = Topico()
        topico.nombre = data['nombre']
        topico.asignatura = profesor.asignatura.id
        topico.save()
        return {'Response':'exito'}

