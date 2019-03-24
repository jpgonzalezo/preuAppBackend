from flask import Flask, Blueprint, jsonify, request
from models.alumno import Alumno
from models.direccion import Direccion
from models.colegio import Colegio
from models.apoderado import Apoderado
from models.curso import Curso
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(AlumnoItem, '/alumno/<id>')
    api.add_resource(Alumnos, '/alumnos')


class AlumnoItem(Resource):
    def get(self, id):
        return json_util.dumps(Alumno.objects(id=id).first().to_json())
        
    def delete(self, id):
        alumno = Alumno.objects(id=id).first()
        alumno.delete()
        return{'Response':'borrado'}


class Alumnos(Resource):
    def get(self):
        alumnos = []
        alumnos_data = Alumno.objects().all()
        for alumno in alumnos_data:
            alumnos.append({
                'id' : str(alumno.id),
                'nombres' : alumno.nombres,
                'apellido_paterno' : alumno.apellido_paterno,
                'apellido_materno' : alumno.apellido_materno,
                'rut' : alumno.rut,
                'curso' : alumno.curso.nombre
            })
        return alumnos

    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        data_personal = data['data_personal']
        data_academico = data['data_academico']
        data_contacto = data['data_contacto']

        alumno = Alumno()
        alumno.nombres = data_personal['nombres']
        alumno.apellido_paterno = data_personal['apellido_paterno']
        alumno.apellido_materno = data_personal['apellido_materno']
        alumno.telefono = data_contacto['telefono']
        alumno.email = data_contacto['email']
        alumno.nombre_usuario = data_personal['nombre_usuario']
        alumno.password = data_personal['password']
        alumno.sexo = data_personal['sexo']
        alumno.rut = data_personal['rut']
        alumno.puntaje_ingreso = data_academico['puntaje_ingreso']
        direccion = Direccion(calle=data_contacto['calle'],
                              numero=data_contacto['numero'],
                              comuna=data_contacto['comuna'])
        alumno.direccion = direccion
        colegio = Colegio.objects(id=data_academico['colegio']).first()
        apoderado = Apoderado.objects(id=data_academico['apoderado']).first()
        curso = Curso.objects(id=data_academico['curso']).first()
        alumno.colegio = colegio
        alumno.apoderado = apoderado
        alumno.curso = curso
        alumno.save()
        return {'Response': 'exito', 
                'nombres':data_personal['nombres'], 
                'apellido_paterno':data_personal['apellido_paterno'], 
                'apellido_materno':data_personal['apellido_materno']}