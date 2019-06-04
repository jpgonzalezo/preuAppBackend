from flask import Flask, Blueprint, jsonify, request
from models.alerta import Alerta
from models.alumno import Alumno
from models.profesor import Profesor
from models.curso import Curso
from models.asignatura import Asignatura
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(AlertaItem, '/alertas/<id>')
    api.add_resource(Alertas, '/alertas')
    api.add_resource(AlertasCurso, '/alertas_curso/<id>')
    api.add_resource(AlertasAlumno, '/alertas_alumno/<id>')
    api.add_resource(AlertasAsignatura, '/alertas_asignatura/<id>')
    api.add_resource(GraficoAlertasCursos, '/alertas/grafico/cursos')

class GraficoAlertasCursos(Resource):
    def get(self):
        labels = []
        data_rendimiento = []
        data_asistencia = []
        for curso in Curso.objects().all():
            if curso.activo:
                labels.append(curso.nombre)
                alertas_rendimiento = 0
                alertas_asistencia = 0
                for alerta in Alerta.objects().all():
                    if alerta.alumno.curso == curso:
                        if alerta.tipo == "RENDIMIENTO":
                            alertas_rendimiento = alertas_rendimiento +1
                        if alerta.tipo == "ASISTENCIA":
                            alertas_asistencia = alertas_asistencia +1
                data_asistencia.append(alertas_asistencia)
                data_rendimiento.append(alertas_rendimiento)

        return {
            "labels": labels,
            "data": [
                {"data": data_rendimiento , "label":"Rendimiento"},
                {"data": data_asistencia, "label": "Asistencia"}
            ]
        }
class AlertasAsignatura(Resource):
    def get(self,id):
        response = []
        asignatura = Asignatura.objects(id=id).first()
        for alerta in Alerta.objects(asignatura=asignatura.id).all():
            response.append(alerta.to_dict())
        return response

class AlertasAlumno(Resource):
    def get(self,id):
        response = []
        alumno = Alumno.objects(id=id).first()
        for alerta in Alerta.objects(alumno=alumno.id).all():
            response.append(alerta.to_dict())
        return response
class AlertaItem(Resource):
    def get(self, id):
        return Alerta.objects(id=id).first().to_dict()

class AlertasCurso(Resource):
    def get(self,id):
        response = []
        curso = Curso.objects(id=id).first()
        for alerta in Alerta.objects().all():
            if str(alerta.alumno.curso.id) == str(id):
                response.append(alerta.to_dict())
        return response

class Alertas(Resource):
    def get(self):
        response = []
        for alerta in Alerta.objects().all():
            response.append(alerta.to_dict())
        return response