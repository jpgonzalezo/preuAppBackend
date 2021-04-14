from flask import Flask, Blueprint, jsonify, request
from models.colegio import Colegio
from models.direccion import Direccion
from models.administrador import Administrador
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.profesor import Profesor
from utils.excel_util import sheet_Tupla as excel_read
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from flask_restful import reqparse

def init_module(api):
    api.add_resource(ColegioItem, '/colegios/<id>')
    api.add_resource(Colegios, '/colegios')
    api.add_resource(ColegiosExcel, '/colegiosExcel/')


class ColegioItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ColegioItem, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return Colegio.objects(id=id).first().to_dict()
    
    def delete(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        colegio = Colegio.objects(id=id).first()
        colegio.activo = False
        colegio.save()
        return {'Response':'exito'}


class Colegios(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(Colegios, self).__init__()
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
        colegios = Colegio.objects().all()
        for colegio in colegios:
            if colegio.activo:
                response.append(colegio.to_dict())
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
        colegio = Colegio()
        colegio.nombre = data['nombre']
        direccion = Direccion()
        direccion.calle = data['calle']
        direccion.numero = data['numero']
        direccion.comuna = data['comuna']
        colegio.direccion = direccion
        colegio.save()
        return {'Response':'exito'}

class ColegiosExcel(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ColegiosExcel, self).__init__()

    def post(self):
        file = request.files["file"]
        lista = excel_read(file)
        print (lista)
        return {'Response': Colegio.create_from_excel(lista)}

