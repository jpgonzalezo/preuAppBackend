from flask import Flask, Blueprint, jsonify, request
from models.prueba import Prueba
from models.asignatura import Asignatura
from models.curso import Curso
from models.evaluacion import Evaluacion
from models.administrador import Administrador
from models.apoderado import Apoderado
from models.alumno import Alumno
from models.profesor import Profesor
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from flask_restful import reqparse

def init_module(api):
    api.add_resource(PruebaItem, '/pruebas/<id>')
    api.add_resource(Pruebas, '/pruebas')
    api.add_resource(PruebasAsignatura, '/pruebas_asignatura/<id>')
    api.add_resource(GraficoRendimientoPreguntas, '/grafico/rendimiento/preguntas/<id>')
    api.add_resource(GraficoRendimientoTopicos, '/grafico/rendimiento/topicos/<id>')
    api.add_resource(GraficoRendimientoCursos, '/grafico/rendimiento/cursos/<id>')

class GraficoRendimientoCursos(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(GraficoRendimientoCursos, self).__init__()
    def get(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        labels=[]
        data = []
        prueba = Prueba.objects(id=id).first()
        for curso in Curso.objects().all():
            if prueba.asignatura in curso.asignaturas:
                cantidad = 0
                promedio = 0
                labels.append(curso.nombre)
                for evaluacion in Evaluacion.objects(prueba=prueba):
                    if evaluacion.alumno.curso == curso:
                        cantidad= cantidad+1
                        promedio = promedio + evaluacion.puntaje
                if cantidad>0:
                    promedio = int(promedio/cantidad)
                data.append(promedio)
        return{
            "labels": labels,
            "data": [data]
        }
class GraficoRendimientoTopicos(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(GraficoRendimientoTopicos, self).__init__()
    def get(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        labels = []
        data = []
        prueba = Prueba.objects(id=id).first()
        for topico in prueba.topicos:
            labels.append(topico.nombre)
        
        for curso in Curso.objects().all():
            if prueba.asignatura in curso.asignaturas:
                data_curso = []
                for topico in prueba.topicos:
                    cantidad_correctas = 0
                    cantidad = 0
                    for pregunta in prueba.preguntas:
                        if topico == pregunta.topico:
                            for evaluacion in Evaluacion.objects(prueba=prueba).all():
                                if evaluacion.alumno.curso == curso:
                                    for respuesta in evaluacion.respuestas:
                                        if respuesta.numero_pregunta == pregunta.numero_pregunta:
                                            cantidad = cantidad + 1
                                            if respuesta.correcta:
                                                cantidad_correctas = cantidad_correctas + 1
                    if cantidad>0:
                        cantidad = int(100*(cantidad_correctas/cantidad))
                    data_curso.append(cantidad)
                data.append({
                    "data": data_curso,
                    "label": curso.nombre
                })

        return {
            "labels":labels,
            "data": data
        }

class GraficoRendimientoPreguntas(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(GraficoRendimientoPreguntas, self).__init__()
    def get(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        labels = []
        data = []
        prueba = Prueba.objects(id=id).first()
        for pregunta in prueba.preguntas:
            labels.append("pregunta "+str(pregunta.numero_pregunta))

        for curso in Curso.objects().all():
            if prueba.asignatura in curso.asignaturas:
                data_curso=[]
                for pregunta in prueba.preguntas:
                    cantidad_correctas = 0
                    cantidad = 0
                    for evaluacion in Evaluacion.objects(prueba=prueba).all():
                        if evaluacion.alumno.curso == curso:
                            for respuesta in evaluacion.respuestas:
                                if respuesta.numero_pregunta == pregunta.numero_pregunta:
                                    cantidad = cantidad + 1
                                    if respuesta.correcta:
                                        cantidad_correctas = cantidad_correctas + 1
                    if cantidad>0:
                        cantidad = int(100*(cantidad_correctas/cantidad))
                    data_curso.append(cantidad)
                data.append({
                    "data": data_curso,
                    "label": curso.nombre
                })
                
        return{
            "labels":labels,
            "data": data
        }
class PruebasAsignatura(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PruebasAsignatura, self).__init__()
    def get(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        response = []
        asignatura = Asignatura.objects(id=id).first()
        for prueba in Prueba.objects(asignatura=asignatura.id):
            response.append(prueba.to_dict())
        return response
class PruebaItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PruebaItem, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return Prueba.objects(id=id).first().to_dict()

class Pruebas(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(Pruebas, self).__init__()
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
        pruebas = Prueba.objects().all()
        for prueba in pruebas:
            if prueba.activo:
                response.append(prueba.to_dict())
        return response