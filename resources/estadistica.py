from flask import Flask, Blueprint, jsonify
from models.alumno import Alumno
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
    api.add_resource(EstadisticaResumen, '/resumen')

class EstadisticaResumen(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(EstadisticaResumen, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        resultado = []
        for asignatura in Asignatura.objects().all():
            data = [0,0,0,0,0,0,0,0,0,0,0,0]
            parcialMes = [0,0,0,0,0,0,0,0,0,0,0,0]
            cantEvaluacion = [0,0,0,0,0,0,0,0,0,0,0,0]
            for evaluacion in Evaluacion.objects(asignatura = asignatura).all():
                indice = int(evaluacion.fecha.strftime("%m"))-1
                parcialMes[ indice] = evaluacion.puntaje + parcialMes[ indice] 
                cantEvaluacion[indice] = cantEvaluacion[indice] +1
            i = 0
            for i in range(cantEvaluacion.__len__()):
                if(cantEvaluacion[i]>0):
                    data[i] = int(parcialMes[i]/cantEvaluacion[i])
            resultado.append({
               'data':data , 
               'label':asignatura.nombre
            })
        return {'asignaturas': resultado }