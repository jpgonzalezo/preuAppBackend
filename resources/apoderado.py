from flask import Flask, Blueprint, jsonify, request, send_file
from models.apoderado import Apoderado
from models.direccion import Direccion
from models.alumno import Alumno
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from PIL import Image
import os

def init_module(api):
    api.add_resource(ApoderadoItem, '/apoderados/<id>')
    api.add_resource(Apoderados, '/apoderados')
    api.add_resource(ApoderadoImagenItem, '/apoderado_imagen/<id>')
    api.add_resource(ApoderadoImagenDefault, '/apoderado_imagen_default/<id>')
    api.add_resource(ApoderadoAsignarAlumno, '/apoderado_alumno/<id_apoderado>/<id_alumno>')
class ApoderadoItem(Resource):
    def get(self, id):
        return json.loads(Apoderado.objects(id=id).first().to_json())

    def delete(self, id):
        apoderado = Apoderado.objects(id=id).first()
        apoderado.activo = False
        apoderado.save()
        return{'Response':'borrado'}


class Apoderados(Resource):
    def get(self):
        apoderados = Apoderado.objects().all()
        response = []
        for apoderado in apoderados:
            if apoderado.activo:
                response.append(apoderado.to_dict())
        return response
    
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        apoderado = Apoderado()
        apoderado.nombres = data['nombres']
        apoderado.apellido_paterno = data['apellido_paterno']
        apoderado.apellido_materno = data['apellido_materno']
        apoderado.telefono = data['telefono']
        apoderado.email = data['email']
        apoderado.password = data['rut']
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
        apoderado = Apoderado.objects(id=id_apoderado).first()
        alumno = Alumno.objects(id=id_alumno).first()
        apoderado.alumno = alumno.id
        apoderado.save()
        return {'Response':'exito'}