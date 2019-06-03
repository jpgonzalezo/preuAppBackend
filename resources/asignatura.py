from flask import Flask, Blueprint, jsonify, request
from models.asignatura import Asignatura
from models.curso import Curso
from models.prueba import Prueba
from models.evaluacion import Evaluacion
from models.asistencia import Asistencia
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(AsignaturaItem, '/asignaturas/<id>')
    api.add_resource(Asignaturas, '/asignaturas')
    api.add_resource(GraficoRendimientoEvaluaciones, '/grafico/rendimiento/evaluaciones/asignatura/<id>')
    api.add_resource(GraficoRendimientoAsistencia, '/grafico/rendimiento/asistencia/asignatura/<id>')

class GraficoRendimientoAsistencia(Resource):
    def get(self,id):
        labels =[]
        data_asistencia = []
        data_inasistencia = []
        asignatura = Asignatura.objects(id=id).first()
        for curso in Curso.objects().all():
            if asignatura in curso.asignaturas:
                labels.append(curso.nombre)
                asistencia_prom = 0
                cantidad_asistencia = 0
                for asistencia in Asistencia.objects(asignatura= asignatura,curso=curso):
                    promedio = 0
                    cantidad_asistencia = cantidad_asistencia +1
                    if len(asistencia.alumnos_presentes) + len(asistencia.alumnos_presentes)>0:
                        promedio = int((len(asistencia.alumnos_presentes)/(len(asistencia.alumnos_presentes) + len(asistencia.alumnos_presentes)))*100)
                    asistencia_prom = asistencia_prom + promedio
                if cantidad_asistencia>0:
                    asistencia_prom = int(asistencia_prom/cantidad_asistencia)
                data_asistencia.append(asistencia_prom)
                data_inasistencia.append(100-asistencia_prom)
        
        return {
            "labels":labels,
            "data": [
                {'data':data_inasistencia,'label':'Inasistencia'},
                {'data':data_asistencia,'label':'Asistencia'}
            ]
        }
class GraficoRendimientoEvaluaciones(Resource):
    def get(self,id):
        labels = []
        data_ensayo = []
        data_taller = []
        data_tarea = []
        asignatura = Asignatura.objects(id=id).first()
        for curso in Curso.objects.all():
            if asignatura in curso.asignaturas:
                labels.append(curso.nombre)

                promedio_ensayo = 0
                for prueba in Prueba.objects(asignatura=asignatura.id, tipo="ENSAYO").all():
                    promedio = 0
                    cant_evaluciones = 0
                    for evaluacion in Evaluacion.objects(prueba=prueba.id).all():
                        if evaluacion.alumno.curso == curso:
                            cant_evaluciones = cant_evaluciones +1
                            promedio = evaluacion.puntaje + promedio
                    if cant_evaluciones>0:
                        promedio = promedio / cant_evaluciones
                    promedio_ensayo = promedio_ensayo + promedio
                if Prueba.objects(asignatura=asignatura.id, tipo="ENSAYO").count():
                    promedio_ensayo = int(promedio_ensayo/Prueba.objects(asignatura=asignatura.id, tipo="ENSAYO").count())
                data_ensayo.append(promedio_ensayo)

                promedio_taller = 0
                for prueba in Prueba.objects(asignatura=asignatura.id, tipo="TALLER").all():
                    promedio = 0
                    cant_evaluciones = 0
                    for evaluacion in Evaluacion.objects(prueba=prueba.id).all():
                        if evaluacion.alumno.curso == curso:
                            cant_evaluciones = cant_evaluciones +1
                            promedio = evaluacion.puntaje + promedio
                    if cant_evaluciones >0:
                        promedio = promedio / cant_evaluciones
                    promedio_taller = promedio_taller + promedio
                if Prueba.objects(asignatura=asignatura.id, tipo="TALLER").count():
                    promedio_taller = int(promedio_taller/Prueba.objects(asignatura=asignatura.id, tipo="ENSAYO").count())
                data_taller.append(promedio_taller)

                promedio_tarea = 0
                for prueba in Prueba.objects(asignatura=asignatura.id, tipo="TAREA").all():
                    promedio = 0
                    cant_evaluciones = 0
                    for evaluacion in Evaluacion.objects(prueba=prueba.id).all():
                        if evaluacion.alumno.curso == curso:
                            promedio = evaluacion.puntaje + promedio
                            cant_evaluciones = cant_evaluciones+1
                    if cant_evaluciones>0:
                        promedio = promedio / cant_evaluciones
                    promedio_tarea = promedio_tarea + promedio
                if Prueba.objects(asignatura=asignatura.id, tipo="TAREA").count():
                    promedio_tarea = int(promedio_tarea/Prueba.objects(asignatura=asignatura.id, tipo="ENSAYO").count())
                data_tarea.append(promedio_tarea)


        return {"labels":labels,
                "data": [
                    {"data": data_ensayo, "label": "Ensayos"},
                    {"data": data_taller, "label": "Talleres"},
                    {"data": data_tarea, "label": "Tareas"},
                ]}
class AsignaturaItem(Resource):
    def get(self, id):
        return json.loads(Asignatura.objects(id=id).first().to_json())
    
    def delete(self,id):
        asignatura = Asignatura.objects(id=id).first()
        asignatura.activo = False
        asignatura.save()
        return {'Response':'exito'}


class Asignaturas(Resource):
    def get(self):
        asignaturas = []
        for asignatura in Asignatura.objects().all():
            if asignatura.activo:
                asignaturas.append(asignatura.to_dict())
        return asignaturas

    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        asignatura = Asignatura()
        asignatura.nombre = data['nombre']
        asignatura.save()
        return {'Response': 'exito'}