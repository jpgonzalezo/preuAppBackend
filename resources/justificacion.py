from flask import Flask, Blueprint, jsonify, request
from models.justificacion import Justificacion
from models.asistencia import Asistencia
from models.alumno import Alumno
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(JustificacionItem, '/justificaciones/<id>')
    api.add_resource(Justificaciones, '/justificaciones')
    api.add_resource(JustificacionesAsistencia, '/justificaciones_asistencia/<id>')
    api.add_resource(JustificacionesAlumno, '/justificaciones_alumno/<id>')

class JustificacionesAlumno(Resource):
    def get(self,id):
        alumno = Alumno.objects(id=id).first()
        justificaciones = []
        for justificacion in Justificacion.objects(alumno=alumno.id).all():
            justificaciones.append(justificacion.to_dict())
        return justificaciones


class JustificacionesAsistencia(Resource):
    def get(self, id):
        asistencia = Asistencia.objects(id=id).first()
        justificaciones = []
        for justificacion in Justificacion.objects(asistencia=asistencia.id).all():
            justificaciones.append(justificacion.to_dict())
        return justificaciones

class JustificacionItem(Resource):
    def get(self, id):
        return Justificacion.objects(id=id).first().to_dict()

class Justificaciones(Resource):
    def get(self):
        response = []
        justificaciones = Justificacion.objects().all()
        for justificacion in justificaciones:
            response.append(justificacion.to_dict())
        return response
    
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        justificacion = Justificacion()
        alumno = Alumno.objects(id=data['id_alumno']).first()
        asistencia = Asistencia.objects(id=data['id_asistencia']).first()
        justificacion.causa = data['causa']
        justificacion.alumno = alumno.id
        justificacion.asistencia = asistencia.id
        justificacion.save()
        return {'Response': 'exito'}