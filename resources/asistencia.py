from flask import Flask, Blueprint, jsonify, request
from models.asistencia import Asistencia
from models.curso import Curso
from models.asignatura import Asignatura
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.administrador import Administrador
from models.profesor import Profesor
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from flask_restful import reqparse

def init_module(api):
    api.add_resource(AsistenciaItem, '/asistencias/<id>')
    api.add_resource(AsistenciaCurso, '/asistencias_curso/<id>')
    api.add_resource(AsistenciaAlumno, '/asistencias_alumno/<id>')
    api.add_resource(AsistenciaAsignatura, '/asistencias_asignatura/<id>')
    api.add_resource(AsistenciaAsignaturaToken, '/asistencias/asignatura')
    api.add_resource(AsistenciaFecha, '/asistencias_fecha/<fecha>')
    api.add_resource(Asistencias, '/asistencias')

class AsistenciaItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AsistenciaItem, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return Asistencia.objects(id=id).first().to_dict()

class AsistenciaCurso(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AsistenciaCurso, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        response = []
        for asistencia in Asistencia.objects(curso=id).all():
            response.append(asistencia.to_dict_short())
        return response

class AsistenciaAlumno(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AsistenciaAlumno, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        response = []
        for asistencia in Asistencia.objects(alumnos_presentes=id).all():
            response.append(asistencia.to_dict())
        return response

class AsistenciaAsignaturaToken(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AsistenciaAsignaturaToken, self).__init__()
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
        for asistencia in Asistencia.objects(asignatura=profesor.asignatura.id).all():
            response.append(asistencia.to_dict())
        return response

class AsistenciaAsignatura(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AsistenciaAsignatura, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        response = []
        for asistencia in Asistencia.objects(asignatura=id).all():
            response.append(asistencia.to_dict_short())
        return response

class AsistenciaFecha(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AsistenciaFecha, self).__init__()
    def get(self, fecha):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        response = []
        for asistencia in Asistencia.objects(fecha=fecha).all():
            print(asistencia.fecha)
            response.append(asistencia.to_dict())
        return response

class Asistencias(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(Asistencias, self).__init__()
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
        for asistencia in Asistencia.objects().all():
            response.append(asistencia.to_dict_short())
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