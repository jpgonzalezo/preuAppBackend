from flask import Flask, Blueprint, jsonify
from models.alumno import Alumno
from models.asignatura import Asignatura
from models.evaluacion import Evaluacion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from datetime import datetime, date, time, timedelta
import calendar

MESES = [
    ("01", "ENERO"),
    ("02", "FEBRERO"),
    ("03", "MARZO"),
    ]

def init_module(api):
    api.add_resource(EstadisticaResumen, '/resumen')

class EstadisticaResumen(Resource):
    def get(self):
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