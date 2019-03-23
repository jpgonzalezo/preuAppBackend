from flask import Flask, Blueprint, jsonify
from models.alumno import Alumno
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(AlumnosItem, '/alumnos/<id>')
    api.add_resource(Alumnos, '/alumnos')


class AlumnosItem(Resource):
    def get(self, id):
        return json_util.dumps(Alumnos.objects(id=id).first().to_json())


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