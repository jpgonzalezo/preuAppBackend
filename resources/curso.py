from flask import Flask, Blueprint, jsonify, request
from models.curso import Curso
from models.asignatura import Asignatura
from models.asistencia import Asistencia
from models.evaluacion import Evaluacion
from models.prueba import Prueba
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(CursoItem, '/cursos/<id>')
    api.add_resource(Cursos, '/cursos')
    api.add_resource(CursoAsignatura, '/curso_asignatura/<id_curso>/<id_asignatura>')
    api.add_resource(CursoGraficoAsistencia, '/curso_grafico_asistencia/<id>')
    api.add_resource(CursoGraficoAsignaturas, '/curso_grafico_asignaturas/<id>')
    api.add_resource(CursoGraficoAsistenciaAsignaturas, '/curso_grafico_asistencia_asignatura/<id>')

class CursoGraficoAsistenciaAsignaturas(Resource):
    def get(self,id):
        curso = Curso.objects(id=id).first()
        labels = []
        asistencia_lista = []
        inasistencia_lista = []
        for asignatura in curso.asignaturas:
            labels.append(asignatura.nombre)
            asistencia_asignatura = 0
            aprobacion = 0
            for asistencia in Asistencia.objects(curso=curso.id, asignatura=asignatura).all():
                asistencia_asignatura = asistencia_asignatura + 1
                aprobacion_asistencia = len(asistencia.alumnos_presentes) /( len(asistencia.alumnos_presentes) + len(asistencia.alumnos_ausentes))
                aprobacion = aprobacion_asistencia + aprobacion
            if asistencia_asignatura> 0:
                aprobacion = int((aprobacion/asistencia_asignatura)*100)
            asistencia_lista.append(aprobacion)
            inasistencia_lista.append(100-aprobacion)
        return {
            "labels":labels,
            "data": [
                {"data": inasistencia_lista, "label": "Inasistencia"},
                {"data": asistencia_lista, "label": "Asistencia"},
            ]
        }

class CursoGraficoAsignaturas(Resource):
    def get(self,id):
        curso = Curso.objects(id=id).first()
        labels = []
        data = []
        for asignatura in curso.asignaturas:
            labels.append(asignatura.nombre)
            suma_parcial_pruebas = 0
            for prueba in Prueba.objects(asignatura = asignatura.id,tipo="ENSAYO").all():
                suma_parcial_evaluaciones = 0
                for evaluacion in Evaluacion.objects(prueba=prueba.id).all():
                    print(evaluacion.alumno.curso)
                    if evaluacion.alumno.curso == curso:
                        suma_parcial_evaluaciones = suma_parcial_evaluaciones + evaluacion.puntaje
                if Evaluacion.objects(prueba=prueba.id).count()>0:
                    suma_parcial_evaluaciones = suma_parcial_evaluaciones/(Evaluacion.objects(prueba=prueba.id).count())
                suma_parcial_evaluaciones = int(suma_parcial_evaluaciones)
                suma_parcial_pruebas = suma_parcial_pruebas + suma_parcial_evaluaciones
            if Prueba.objects(asignatura = asignatura.id,tipo="ENSAYO").count()>0:
                suma_parcial_pruebas = int(suma_parcial_pruebas/(Prueba.objects(asignatura = asignatura.id,tipo="ENSAYO").count()))
            data.append(suma_parcial_pruebas)
        return {
            "labels":labels,
            "data": data
        }
class CursoGraficoAsistencia(Resource):
    def get(self,id):
        curso = Curso.objects(id=id).first()
        labels = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
        meses = [1,2,3,4,5,6,7,8,9,10,11,12]
        asistencia_lista = []
        inasistencia_lista = []
        for mes in meses:
            asistencia_mes = 0
            aprobacion = 0
            for asistencia in Asistencia.objects(curso=curso.id).all():
                if str(asistencia.fecha.month) == str(mes):
                    asistencia_mes = asistencia_mes + 1
                    aprobacion_asistencia = len(asistencia.alumnos_presentes) /( len(asistencia.alumnos_presentes) + len(asistencia.alumnos_ausentes))
                    aprobacion = aprobacion_asistencia + aprobacion
            if asistencia_mes> 0:
                aprobacion = int((aprobacion/asistencia_mes)*100)
            asistencia_lista.append(aprobacion)
            inasistencia_lista.append(100-aprobacion)
        return {
            "labels":labels,
            "data": [
                {"data": inasistencia_lista, "label": "Inasistencia"},
                {"data": asistencia_lista, "label": "Asistencia"},
            ]
        }
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
