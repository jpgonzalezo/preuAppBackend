from flask import Flask, Blueprint, jsonify
from models.asistencia import Asistencia
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(AsistenciaItem, '/asistencia/<id>')
    api.add_resource(AsistenciaCurso, '/asistencias_curso/<id>')
    api.add_resource(AsistenciaAlumno, '/asistencias_alumno/<id>')
    api.add_resource(AsistenciaAsignatura, '/asistencias_asignatura/<id>')
    api.add_resource(AsistenciaFecha, '/asistencias_fecha/<fecha>')
    api.add_resource(Asistencias, '/asistencias')


class AsistenciaItem(Resource):
    def get(self, id):
        return json.loads(Asistencia.objects(id=id).first().to_json())

class AsistenciaCurso(Resource):
    def get(self, id):
        response = []
        for asistencia in Asistencia.objects(curso=id).all():
            response.append(asistencia.to_dict())
        return response

#TODO: ver como buscar en las 2 listas
class AsistenciaAlumno(Resource):
    def get(self, id):
        response = []
        for asistencia in Asistencia.objects(alumnos_presentes=id).all():
            response.append(asistencia.to_dict())
        return response

class AsistenciaAsignatura(Resource):
    def get(self, id):
        response = []
        for asistencia in Asistencia.objects(asignatura=id).all():
            print(asistencia.fecha)
            response.append(asistencia.to_dict())
        return response

#TODO: ver formato fecha
class AsistenciaFecha(Resource):
    def get(self, fecha):
        response = []
        for asistencia in Asistencia.objects(fecha=fecha).all():
            print(asistencia.fecha)
            response.append(asistencia.to_dict())
        return response

class Asistencias(Resource):
    def get(self):
        response = []
        for asistencia in Asistencia.objects().all():
            response.append(asistencia.to_dict())
        return response