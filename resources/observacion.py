from flask import Flask, Blueprint, jsonify, request
from models.observacion import Observacion, ObservacionProfesor
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
    api.add_resource(ObservacionItem, '/observacion/<id>')
    api.add_resource(Observaciones, '/observaciones')
    api.add_resource(ObservacionAlumno, '/observaciones_alumno/<id>/<tipo>')
    api.add_resource(ObservacionProfesor_, '/observaciones/profesor/<id_profesor>')


class ObservacionItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ObservacionItem, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return json.loads(Observacion.objects(id=id).first().to_json())

class ObservacionAlumno(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ObservacionAlumno, self).__init__()
    def get(self,id,tipo):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        response = []
        observaciones = Observacion.objects(alumno=id,tipo=tipo).all()
        for observacion in observaciones:
            response.append(observacion.to_dict())
        return response

class Observaciones(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(Observaciones, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return json.loads(Observacion.objects().all().to_json())
    
    def post(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        data = request.data.decode()
        data = json.loads(data)
        observacion = Observacion()
        observacion.titulo = data['titulo']
        observacion.contenido = data['contenido']
        observacion.tipo = data['tipo']
        if administrador != None:
            observacion.nombre_personal = administrador.nombres+" "+administrador.apellido_paterno+" "+administrador.apellido_materno
        if profesor != None:
            observacion.nombre_personal = profesor.nombres+" "+profesor.apellido_paterno+" "+profesor.apellido_materno
        observacion.alumno = Alumno.objects(id=data['alumno']).first()
        observacion.save()
        return {'Response': 'exito'}

class ObservacionProfesor_(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ObservacionProfesor_, self).__init__()
    
    def post(self,id_profesor):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        profesor = Profesor.objects(id=id_profesor).first()
        if alumno == None and profesor == None:
            return {'response': 'user_invalid'},401
        data = request.data.decode()
        data = json.loads(data)
        observacion = ObservacionProfesor()
        observacion.titulo = data['titulo']
        observacion.contenido = data['contenido']
        observacion.anonimo = data['tipo']

        observacion.alumno = alumno.id
        observacion.profesor = profesor.id
        observacion.save()
        return {'Response': 'exito'}
    
