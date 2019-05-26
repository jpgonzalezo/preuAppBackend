from flask import Flask, Blueprint, jsonify, request
from models.alerta import Alerta
from models.alumno import Alumno
from models.profesor import Profesor
from models.curso import Curso
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(AlertaItem, '/alertas/<id>')
    api.add_resource(Alertas, '/alertas')
    api.add_resource(AlertasCurso, '/alertas_curso/<id>')
    api.add_resource(AlertasAlumno, '/alertas_alumno/<id>')
    

class AlertasAlumno(Resource):
    def get(self,id):
        response = []
        alumno = Alumno.objects(id=id).first()
        for alerta in Alerta.objects(alumno=alumno.id).all():
            response.append(alerta.to_dict())
        return response
class AlertaItem(Resource):
    def get(self, id):
        return Alerta.objects(id=id).first().to_dict()

class AlertasCurso(Resource):
    def get(self,id):
        response = []
        curso = Curso.objects(id=id).first()
        for alerta in Alerta.objects().all():
            if str(alerta.alumno.curso.id) == str(id):
                response.append(alerta.to_dict())
        return response

class Alertas(Resource):
    def get(self):
        response = []
        for alerta in Alerta.objects().all():
            response.append(alerta.to_dict())
        return response