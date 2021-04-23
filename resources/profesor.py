from flask import Flask, Blueprint, jsonify, request, send_file
from models.profesor import Profesor
from models.direccion import Direccion
from models.asignatura import Asignatura
from models.alumno import Alumno
from models.administrador import Administrador
from models.apoderado import Apoderado
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from PIL import Image
from flask_restful import reqparse
import os

def init_module(api):
    api.add_resource(ProfesorItem, '/profesores/<id>')
    api.add_resource(Profesores, '/profesores')
    api.add_resource(ProfesorImagenItem, '/profesor_imagen/<id>')
    api.add_resource(ProfesorImagenDefault, '/profesor_imagen_default/<id>')
    api.add_resource(ProfesoresAsignatura, '/profesores_asignatura/<id_asignatura>')
    api.add_resource(ProfesoresAsignaturaToken, '/profesores/asignatura')
    

class ProfesoresAsignaturaToken(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ProfesoresAsignaturaToken, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        profesores = []
        asignatura = Asignatura.objects(id=profesor.asignatura.id).first()
        for profesor in Profesor.objects(asignatura=asignatura.id, activo=True).all():
            if profesor.activo:
                profesores.append(profesor.to_dict())
        return profesores

class ProfesoresAsignatura(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ProfesoresAsignatura, self).__init__()
    def get(self,id_asignatura):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        profesores = []
        asignatura = Asignatura.objects(id=id_asignatura).first()
        for profesor in Profesor.objects(asignatura=asignatura.id, activo=True).all():
            if profesor.activo:
                profesores.append(profesor.to_dict())
        return profesores

class ProfesorItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ProfesorItem, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return Profesor.objects(id=id).first().to_dict()
    
    def delete(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        profesor = Profesor.objects(id=id).first()
        profesor.activo = False
        profesor.save()
        return{'Response':'borrado'}
    
    def put(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.objects(id=id).first()
        if administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        data = request.data.decode()
        data = json.loads(data)
        profesor.nombres = data['nombres']
        profesor.apellido_paterno = data['apellido_paterno']
        profesor.apellido_materno = data['apellido_materno']
        profesor.telefono = data['telefono']
        profesor.email = data['email']
        profesor.rut = data['rut']
        direccion = Direccion(calle=data['calle'],
                              numero=data['numero'],
                              comuna=data['comuna'],
                              cas_dep_of=data['cas_dep_of'])
        profesor.direccion = direccion
        asignatura = Asignatura.objects(id=data['asignatura']).first()
        profesor.asignatura = asignatura.id
        profesor.save()
        return {'Response': 'exito',
                'id': str(profesor.id)}

class Profesores(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(Profesores, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        profesores = Profesor.objects().all()
        response = []
        for profesor in profesores:
            if profesor.activo:
                response.append(profesor.to_dict())
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
        profesor = Profesor()
        profesor.nombres = data['nombres']
        profesor.apellido_paterno = data['apellido_paterno']
        profesor.apellido_materno = data['apellido_materno']
        profesor.telefono = data['telefono']
        profesor.email = data['email']
        profesor.encrypt_password(data['rut'])
        profesor.rut = data['rut']
        direccion = Direccion(calle=data['calle'],
                              numero=data['numero'],
                              comuna=data['comuna'],
                              cas_dep_of=data['cas_dep_of'])
        profesor.direccion = direccion
        asignatura = Asignatura.objects(id=data['asignatura']).first()
        profesor.asignatura = asignatura.id
        profesor.save()
        return {'Response': 'exito',
                'id': str(profesor.id)}

class ProfesorImagenItem(Resource):
    def post(self,id):
        profesor = Profesor.open(request.files['imagen'].stream).convert("RGB")
        profesor.save(os.path.join("./uploads/profesores", str(id)+".jpg"))
        profesor.thumbnail((800, 800))
        profesor.save(os.path.join("./uploads/profesores", str(id)+'_thumbnail.jpg'))
        profesor = Profesor.objects(id=id).first()
        profesor.imagen = id
        profesor.save()
        return {'Response': 'exito'}
    
    def get(self,id):
        return send_file('uploads/profesores/'+id+'_thumbnail.jpg')

class ProfesorImagenDefault(Resource):
    def get(self,id):
        profesor = Profesor.objects(id=id).first()
        imagen = Image.open("./uploads/profesores/default_thumbnail.jpg")
        imagen.thumbnail((800, 800))
        imagen.save(os.path.join("./uploads/profesores", str(id)+'_thumbnail.jpg'))
        profesor.imagen = str(profesor.id)
        profesor.save()
        return { 'Response':'exito'}