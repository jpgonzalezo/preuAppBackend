from flask import Flask, Blueprint, jsonify, request
from models.alumno import Alumno
from models.archivo import Archivo
from models.administrador import Administrador
from models.apoderado import Apoderado
from models.profesor import Profesor
from models.asignatura import Asignatura
from models.evaluacion import Evaluacion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from datetime import datetime, date, time, timedelta
import calendar
from flask_restful import reqparse

def init_module(api):
    api.add_resource(ArchivoAsignatura, '/archivoAsignatura/<asignatura_id>')
    api.add_resource(ArchivoDescarga, '/download/<archivo_id>')


class ArchivoAsignatura(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ArchivoAsignatura, self).__init__()

    def post(self,asignatura_id):
        file = request.files["file"]
        return {'Response': Archivo.upload(file , asignatura_id)}

    def get(self, asignatura_id):
        return Archivo.get_all_by_asignatura(asignatura_id)

class ArchivoDescarga(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ArchivoDescarga, self).__init__()

    def get(self,archivo_id):
        return Archivo.download(archivo_id)

