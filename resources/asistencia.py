from flask import Flask, Blueprint, jsonify, request
from models.asistencia import Asistencia
from models.curso import Curso
from models.asignatura import Asignatura
from models.alumno import Alumno
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(AsistenciaItem, '/asistencias/<id>')
    api.add_resource(AsistenciaCurso, '/asistencias_curso/<id>')
    api.add_resource(AsistenciaAlumno, '/asistencias_alumno/<id>')
    api.add_resource(AsistenciaAsignatura, '/asistencias_asignatura/<id>')
    api.add_resource(AsistenciaFecha, '/asistencias_fecha/<fecha>')
    api.add_resource(Asistencias, '/asistencias')


class AsistenciaItem(Resource):
    def get(self, id):
        return Asistencia.objects(id=id).first().to_dict()

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
    
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        curso = Curso.objects(id = data['id_curso']).first()
        asignatura = Asignatura.objects(id=data['id_asignatura']).first()
        asistencia = Asistencia()
        asistencia.curso = curso.id
        asistencia.asignatura = asignatura.id
        for alumno in data['presentes']:
            alumno_aux = Alumno.objects(id=alumno['id']).first()
            asistencia.alumnos_presentes.append(alumno_aux.id)
        for alumno in data['ausentes']:
            alumno_aux = Alumno.objects(id=alumno['id']).first()
            asistencia.alumnos_ausentes.append(alumno_aux.id)
        asistencia.save()
        return {'Response': 'exito'}