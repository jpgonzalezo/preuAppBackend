from flask import Flask, Blueprint, jsonify, request, send_file
from models.administrador import Administrador
from models.direccion import Direccion
from models.alerta import Alerta
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from PIL import Image
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
    def get(self, id):
        return json.loads(Administrador.objects(id=id).first().to_json())

    def delete(self, id):
        administrador = Administrador.objects(id=id).first()
        administrador.activo = False
        administrador.save()
        return{'Response':'borrado'}


class Administradores(Resource):
    def get(self):
        administradores = Administrador.objects().all()
        response = []
        for administrador in administradores:
            if administrador.activo:
                response.append(administrador.to_dict())
        return response
    
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        administrador = Administrador()
        administrador.nombres = data['nombres']
        administrador.apellido_paterno = data['apellido_paterno']
        administrador.apellido_materno = data['apellido_materno']
        administrador.telefono = data['telefono']
        administrador.email = data['email']
        administrador.rut = data['rut']
        administrador.password = data['rut']
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