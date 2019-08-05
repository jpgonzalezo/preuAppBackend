from flask import Flask, Blueprint, jsonify, request
from models.justificacion import Justificacion
from models.asistencia import Asistencia
from models.alumno import Alumno
from models.administrador import Administrador
from models.apoderado import Apoderado
from models.profesor import Profesor
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from flask_restful import reqparse

def init_module(api):
    api.add_resource(JustificacionItem, '/justificaciones/<id>')
    api.add_resource(Justificaciones, '/justificaciones')
    api.add_resource(JustificacionesAsistencia, '/justificaciones_asistencia/<id>')
    api.add_resource(JustificacionesAlumno, '/justificaciones_alumno/<id>')

class JustificacionesAlumno(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(JustificacionesAlumno, self).__init__()
    def get(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        alumno = Alumno.objects(id=id).first()
        justificaciones = []
        for justificacion in Justificacion.objects(alumno=alumno.id).all():
            if justificacion.activo:
                justificaciones.append(justificacion.to_dict())
        return justificaciones


class JustificacionesAsistencia(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(JustificacionesAsistencia, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        asistencia = Asistencia.objects(id=id).first()
        justificaciones = []
        for justificacion in Justificacion.objects(asistencia=asistencia.id).all():
            if justificacion.activo:
                justificaciones.append(justificacion.to_dict())
        return justificaciones

class JustificacionItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(JustificacionItem, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return Justificacion.objects(id=id).first().to_dict()
    def delete(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        justificacion = Justificacion.objects(id=id).first()
        justificacion.activo = False
        justificacion.save()
        return {'Response':'exito'}

class Justificaciones(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(Justificaciones, self).__init__()
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
        justificaciones = Justificacion.objects().all()
        for justificacion in justificaciones:
            if justificacion.activo:
                response.append(justificacion.to_dict())
        return response
    
    def post(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
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