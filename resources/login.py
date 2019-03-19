from flask import Flask, Blueprint, jsonify, request
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.administrador import Administrador
from models.profesor import Profesor
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(Login, '/login')


class Login(Resource):
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        data = data['data']
        alumno = Alumno.objects(nombre_usuario = data['nombre_usuario'], password = data['password']).first()
        apoderado = Apoderado.objects(nombre_usuario = data['nombre_usuario'], password = data['password']).first()
        profesor = Profesor.objects(nombre_usuario = data['nombre_usuario'], password = data['password']).first()
        administrador = Administrador.objects(nombre_usuario = data['nombre_usuario'], password = data['password']).first()
    
        if(apoderado != None):
            return {'respuesta': {'tipo': 'apoderado', 'usuario':json.loads(apoderado.to_json())}}
        elif(alumno != None):
            return {'respuesta': {'tipo': 'alumno', 'usuario': json.loads(alumno.to_json())}}
        elif(administrador != None):
            return {'respuesta': {'tipo': 'administrador', 'usuario': json.loads(administrador.to_json())}}
        elif(profesor != None):
            return {'respuesta': {'tipo': 'profesor', 'usuario':json.loads(profesor.to_json())}}
        else:
            return {'respuesta': {'tipo': 'no_existe', 'usuario':""}}