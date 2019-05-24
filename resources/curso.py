from flask import Flask, Blueprint, jsonify, request
from models.curso import Curso
from models.asignatura import Asignatura
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(CursoItem, '/cursos/<id>')
    api.add_resource(Cursos, '/cursos')
    api.add_resource(CursoAsignatura, '/curso_asignatura/<id_curso>/<id_asignatura>')


class CursoAsignatura(Resource):
    def put(self,id_curso,id_asignatura):
        asignatura = Asignatura.objects(id=id_asignatura).first()
        curso = Curso.objects(id=id_curso).first()
        curso.asignaturas.append(asignatura.id)
        curso.save()
        return { 'Response': "exito"}

    def delete(self,id_curso,id_asignatura):
        asignatura = Asignatura.objects(id=id_asignatura).first()
        curso = Curso.objects(id=id_curso).first()
        curso.asignaturas.remove(asignatura)
        curso.save()
        return { 'Response': "exito"}

class CursoItem(Resource):
    def get(self, id):
        return Curso.objects(id=id).first().to_dict()

    def delete(self,id):
        curso = Curso.objects(id=id).first()
        curso.activo = False
        curso.save()
        return {'Response':'exito'}


class Cursos(Resource):
    def get(self):
        cursos = []
        for curso in Curso.objects().all():
            if curso.activo:
                cursos.append(curso.to_dict())
        return cursos
    
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        curso = Curso()
        curso.nombre = data['nombre']
        curso.save()
        return {'Response': 'exito'}
