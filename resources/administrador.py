from flask import Flask, Blueprint, jsonify, request, send_file
from models.administrador import Administrador
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.profesor import Profesor
from models.direccion import Direccion
from models.alerta import Alerta
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from PIL import Image
from flask_restful import reqparse
import os

def init_module(api):
    api.add_resource(AdministradorItem, '/administradores/<id>')
    api.add_resource(Administradores, '/administradores')
    api.add_resource(AdministradorImagenItem, '/administrador_imagen/<id>')
    api.add_resource(AdministradorImagenDefault, '/administrador_imagen_default/<id>')

def administradorEncriptacion():
    for administrador in Administrador.objects().all():
        administrador.encrypt_password(administrador.password)
        administrador.save()
class AdministradorItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AdministradorItem, self).__init__()

    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return Administrador.objects(id=id).first().to_dict()

    def delete(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        administrador = Administrador.objects(id=id).first()
        administrador.activo = False
        administrador.save()
        return{'Response':'borrado'}


class Administradores(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(Administradores, self).__init__()

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
        for administrador in Administrador.objects(activo=True).all():
            if administrador.activo:
                response.append(administrador.to_dict())
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
        administrador = Administrador()
        administrador.nombres = data['nombres']
        administrador.apellido_paterno = data['apellido_paterno']
        administrador.apellido_materno = data['apellido_materno']
        administrador.telefono = data['telefono']
        administrador.email = data['email']
        administrador.rut = data['rut']
        administrador.encrypt_password(data['rut'])
        administrador.save()
        return {'Response': 'exito',
                'id': str(administrador.id)}

class AdministradorImagenItem(Resource):
    def post(self,id):
        imagen = Image.open(request.files['imagen'].stream).convert("RGB")
        imagen.save(os.path.join("./uploads/administradores", str(id)+".jpg"))
        imagen.thumbnail((800, 800))
        imagen.save(os.path.join("./uploads/administradores", str(id)+'_thumbnail.jpg'))
        administrador = Administrador.objects(id=id).first()
        administrador.imagen = id
        administrador.save()
        return {'Response': 'exito','id': str(administrador.id)}
    
    def get(self,id):
        return send_file('./uploads/administradores/'+id+'_thumbnail.jpg')

class AdministradorImagenDefault(Resource):
    def get(self,id):
        administrador = Administrador.objects(id=id).first()
        imagen = Image.open("./uploads/administradores/default_thumbnail.jpg")
        imagen.thumbnail((800, 800))
        imagen.save(os.path.join("./uploads/administradores", str(id)+'_thumbnail.jpg'))
        administrador.imagen = str(administrador.id)
        administrador.save()
        return { 'Response':'exito'}