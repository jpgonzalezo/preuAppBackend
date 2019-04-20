from flask import Flask, Blueprint, jsonify, request, send_file
from models.profesor import Profesor
from models.direccion import Direccion
from models.asignatura import Asignatura
from models.alumno import Alumno
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from PIL import Image
import os

def init_module(api):
    api.add_resource(ProfesorItem, '/profesores/<id>')
    api.add_resource(Profesores, '/profesores')
    api.add_resource(ProfesorImagenItem, '/profesor_imagen/<id>')
    api.add_resource(ProfesorImagenDefault, '/profesor_imagen_default/<id>')
    
class ProfesorItem(Resource):
    def get(self, id):
        return json.loads(Profesor.objects(id=id).first().to_json())
    
    def delete(self, id):
        profesor = Profesor.objects(id=id).first()
        profesor.activo = False
        profesor.save()
        return{'Response':'borrado'}

class Profesores(Resource):
    def get(self):
        profesores = Profesor.objects().all()
        response = []
        for profesor in profesores:
            if profesor.activo:
                response.append(profesor.to_dict())
        return response
    
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        profesor = Profesor()
        profesor.nombres = data['nombres']
        profesor.apellido_paterno = data['apellido_paterno']
        profesor.apellido_materno = data['apellido_materno']
        profesor.telefono = data['telefono']
        profesor.email = data['email']
        profesor.password = data['rut']
        profesor.rut = data['rut']
        direccion = Direccion(calle=data['calle'],
                              numero=data['numero'],
                              comuna=data['comuna'])
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
        profesor.imagen = "default"
        profesor.save()
        return { 'Response':'exito'}