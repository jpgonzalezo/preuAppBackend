from flask import Flask, Blueprint, jsonify, request, send_file
from models.apoderado import Apoderado
from models.direccion import Direccion
from models.alumno import Alumno
from models.administrador import Administrador
from models.profesor import Profesor
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from PIL import Image
from flask_restful import reqparse
import os

def init_module(api):
    api.add_resource(ApoderadoItem, '/apoderados/<id>')
    api.add_resource(Apoderados, '/apoderados')
    api.add_resource(ApoderadoImagenItem, '/apoderado_imagen/<id>')
    api.add_resource(ApoderadoImagenDefault, '/apoderado_imagen_default/<id>')
    api.add_resource(ApoderadoAsignarAlumno, '/apoderado_alumno/<id_apoderado>/<id_alumno>')
class ApoderadoItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ApoderadoItem, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return Apoderado.objects(id=id).first().to_dict()

    def delete(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        apoderado = Apoderado.objects(id=id).first()
        apoderado.activo = False
        apoderado.save()
        return{'Response':'borrado'}


class Apoderados(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(Apoderados, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        apoderados = Apoderado.objects(activo=True).all()
        response = []
        for apoderado in apoderados:
            if apoderado.activo:
                response.append(apoderado.to_dict())
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
        apoderado = Apoderado()
        apoderado.nombres = data['nombres']
        apoderado.apellido_paterno = data['apellido_paterno']
        apoderado.apellido_materno = data['apellido_materno']
        apoderado.telefono = data['telefono']
        apoderado.email = data['email']
        apoderado.encrypt_password(data['rut'])
        apoderado.rut = data['rut']
        direccion = Direccion(calle=data['calle'],
                              numero=data['numero'],
                              comuna=data['comuna'])
        apoderado.direccion = direccion
        apoderado.save()
        return {'Response': 'exito',
                'id': str(apoderado.id)}

class ApoderadoImagenItem(Resource):
    def post(self,id):
        imagen = Image.open(request.files['imagen'].stream).convert("RGB")
        imagen.save(os.path.join("./uploads/apoderados", str(id)+".jpg"))
        imagen.thumbnail((800, 800))
        imagen.save(os.path.join("./uploads/apoderados", str(id)+'_thumbnail.jpg'))
        apoderado = Apoderado.objects(id=id).first()
        apoderado.imagen = id
        apoderado.save()
        return {'Response': 'exito','id': str(apoderado.id)}
    
    def get(self,id):
        return send_file('uploads/apoderados/'+id+'_thumbnail.jpg')

class ApoderadoImagenDefault(Resource):
    def get(self,id):
        apoderado = Apoderado.objects(id=id).first()
        apoderado.imagen = "default"
        apoderado.save()
        return { 'Response':'exito','id': str(apoderado.id)}

class ApoderadoAsignarAlumno(Resource):
    def get(self,id_apoderado,id_alumno):
        apoderado = Apoderado.objects(id=id).first()
        imagen = Image.open("./uploads/apoderados/default_thumbnail.jpg")
        imagen.thumbnail((800, 800))
        imagen.save(os.path.join("./uploads/apoderados", str(id)+'_thumbnail.jpg'))
        apoderado.imagen = str(apoderado.id)
        apoderado.save()
        return { 'Response':'exito'}