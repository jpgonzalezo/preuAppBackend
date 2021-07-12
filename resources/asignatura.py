from flask import Flask, Blueprint, jsonify, request
from models.asignatura import Asignatura
from models.curso import Curso
from models.prueba import Prueba
from models.evaluacion import Evaluacion
from models.asistencia import Asistencia
from models.administrador import Administrador
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.profesor import Profesor
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from flask_restful import reqparse

def init_module(api):
    api.add_resource(AsignaturaItem, '/asignaturas/<id>')
    api.add_resource(Asignaturas, '/asignaturas')
    api.add_resource(AsignaturaToken, '/asignatura')
    api.add_resource(AsignaturasCurso, '/asignaturas/curso/<id>')
    api.add_resource(AsignaturaCursos, '/asignatura/cursos')
    api.add_resource(GraficoRendimientoEvaluaciones, '/grafico/rendimiento/evaluaciones/asignatura/<id>')
    api.add_resource(GraficoRendimientoEvaluacionesToken, '/grafico/rendimiento/evaluaciones/asignatura')
    api.add_resource(GraficoRendimientoAsistencia, '/grafico/rendimiento/asistencia/asignatura/<id>')
    api.add_resource(GraficoRendimientoAsistenciaToken, '/grafico/rendimiento/asistencia/asignatura')


class AsignaturaCursos(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AsignaturaCursos, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        cursos = []
        if profesor == None:
            return {'response': 'user_invalid'},401
        for curso in Curso.objects().all():
            if profesor.asignatura in curso.asignaturas:
                cursos.append({
                    "id": str(curso.id),
                    "nombre": str(curso.nombre)
                })
        return cursos


class GraficoRendimientoAsistenciaToken(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(GraficoRendimientoAsistenciaToken, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        labels =[]
        data_asistencia = []
        data_inasistencia = []
        asignatura = Asignatura.objects(id=profesor.asignatura.id).first()
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
                {'data':data_asistencia,'label':'Asistencia'}
            ]
        }

class GraficoRendimientoAsistencia(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(GraficoRendimientoAsistencia, self).__init__()
    def get(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        labels =[]
        data_asistencia = []
        data_inasistencia = []
        asignatura = Asignatura.objects(id=id).first()
        for curso in Curso.objects().all():
            if asignatura in curso.asignaturas:
                labels.append(curso.nombre)
                asistencia_prom = 0
                cantidad_asistencia = 0
                for asistencia in Asistencia.objects(asignatura= asignatura,curso=curso).all():
                    promedio = 0
                    cantidad_asistencia = cantidad_asistencia +1
                    if len(asistencia.alumnos_presentes) + len(asistencia.alumnos_presentes)>0:
                        promedio = int( (len(asistencia.alumnos_presentes) / ( len(asistencia.alumnos_presentes) + len(asistencia.alumnos_presentes) ) )*100)
                    asistencia_prom = asistencia_prom + promedio
                if cantidad_asistencia>0:
                    asistencia_prom = int(asistencia_prom/cantidad_asistencia)
                data_asistencia.append(asistencia_prom)
                data_inasistencia.append(100-asistencia_prom)
        
        return {
            "labels":labels,
            "data": [
                {'data':data_asistencia,'label':'Asistencia'}
            ]
        }

class GraficoRendimientoEvaluacionesToken(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(GraficoRendimientoEvaluacionesToken, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        labels = []
        data_ensayo = []
        data_taller = []
        data_tarea = []
        asignatura = Asignatura.objects(id=profesor.asignatura.id).first()
        for curso in Curso.objects.all():
            if asignatura in curso.asignaturas:
                labels.append(curso.nombre)

                promedio_ensayo = 0
                cantidad_ensayo_con_evaluaciones = 0
                for prueba in Prueba.objects(asignatura=asignatura.id, tipo="ENSAYO").all():
                    evaluaciones = Evaluacion.objects(prueba=prueba.id).all()
                    if len(evaluaciones)>0:
                        cant_evaluciones = 0
                        promedio = 0
                        banderaEvaluacionesCurso = False
                        for evaluacion in evaluaciones:
                            if evaluacion.alumno.curso == curso:
                                banderaEvaluacionesCurso = True
                                cant_evaluciones = cant_evaluciones +1
                                promedio = evaluacion.puntaje + promedio
                        if cant_evaluciones>0:
                            promedio = int(promedio / cant_evaluciones)
                        if banderaEvaluacionesCurso:
                            cantidad_ensayo_con_evaluaciones = cantidad_ensayo_con_evaluaciones + 1
                        promedio_ensayo = promedio_ensayo + promedio
                if cantidad_ensayo_con_evaluaciones>0:
                    promedio_ensayo = int(promedio_ensayo/cantidad_ensayo_con_evaluaciones)
                data_ensayo.append(promedio_ensayo)

                promedio_taller = 0
                cantidad_taller_con_evaluaciones = 0
                for prueba in Prueba.objects(asignatura=asignatura.id, tipo="TALLER").all():
                    evaluaciones = Evaluacion.objects(prueba=prueba.id).all()
                    if len(evaluaciones)>0:
                        promedio = 0
                        cant_evaluciones = 0
                        banderaEvaluacionesCurso = False
                        for evaluacion in evaluaciones:
                            if evaluacion.alumno.curso == curso:
                                banderaEvaluacionesCurso = True
                                cant_evaluciones = cant_evaluciones +1
                                promedio = evaluacion.puntaje + promedio
                        if cant_evaluciones >0:
                            promedio = promedio / cant_evaluciones
                        promedio_taller = promedio_taller + promedio
                        if banderaEvaluacionesCurso:
                            cantidad_taller_con_evaluaciones = cantidad_taller_con_evaluaciones + 1
                if cantidad_taller_con_evaluaciones>0:
                    promedio_taller = int(promedio_taller/cantidad_taller_con_evaluaciones)
                data_taller.append(promedio_taller)

                promedio_tarea = 0
                cantidad_tarea_con_evaluaciones = 0
                for prueba in Prueba.objects(asignatura=asignatura.id, tipo="TAREA").all():
                    evaluaciones = Evaluacion.objects(prueba=prueba.id).all()
                    if len(evaluaciones)>0:
                        
                        promedio = 0
                        cant_evaluciones = 0
                        banderaEvaluacionesCurso = False
                        for evaluacion in evaluaciones:
                            if evaluacion.alumno.curso == curso:
                                promedio = evaluacion.puntaje + promedio
                                cant_evaluciones = cant_evaluciones+1
                                banderaEvaluacionesCurso = True
                        if cant_evaluciones>0:
                            promedio = promedio / cant_evaluciones
                        promedio_tarea = promedio_tarea + promedio
                        if banderaEvaluacionesCurso:
                            cantidad_tarea_con_evaluaciones = cantidad_tarea_con_evaluaciones + 1
                if cantidad_tarea_con_evaluaciones:
                    promedio_tarea = int(promedio_tarea/cantidad_tarea_con_evaluaciones)
                data_tarea.append(promedio_tarea)


        return {"labels":labels,
                "data": [
                    {"data": data_ensayo, "label": "Puntos ensayos"},
                    {"data": data_taller, "label": "Puntos talleres"},
                    {"data": data_tarea, "label": "Puntos tareas"},
                ]}

class GraficoRendimientoEvaluaciones(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(GraficoRendimientoEvaluaciones, self).__init__()
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
        data_ensayo = []
        data_taller = []
        data_tarea = []
        asignatura = Asignatura.objects(id=id).first()
        for curso in Curso.objects.all():
            if asignatura in curso.asignaturas:
                labels.append(curso.nombre)

                promedio_ensayo = 0
                cantidad_ensayo_con_evaluaciones = 0
                for prueba in Prueba.objects(asignatura=asignatura.id, tipo="ENSAYO").all():
                    evaluaciones = Evaluacion.objects(prueba=prueba.id).all()
                    if evaluaciones:
                        promedio = 0
                        cant_evaluciones = 0
                        banderaEvaluacionesCurso = False
                        for evaluacion in Evaluacion.objects(prueba=prueba.id).all():
                            if evaluacion.alumno.curso == curso:
                                cant_evaluciones = cant_evaluciones +1
                                promedio = evaluacion.puntaje + promedio
                                banderaEvaluacionesCurso = True
                        if cant_evaluciones>0:
                            promedio = promedio / cant_evaluciones
                        promedio_ensayo = promedio_ensayo + promedio
                        if banderaEvaluacionesCurso:
                            cantidad_ensayo_con_evaluaciones = cantidad_ensayo_con_evaluaciones + 1
                if cantidad_ensayo_con_evaluaciones:
                    promedio_ensayo = int(promedio_ensayo/cantidad_ensayo_con_evaluaciones)
                data_ensayo.append(promedio_ensayo)

                promedio_taller = 0
                cantidad_taller_con_evaluaciones = 0
                for prueba in Prueba.objects(asignatura=asignatura.id, tipo="TALLER").all():
                    evaluaciones = Evaluacion.objects(prueba=prueba.id).all()
                    if evaluaciones:
                        promedio = 0
                        cant_evaluciones = 0
                        banderaEvaluacionesCurso = False
                        for evaluacion in Evaluacion.objects(prueba=prueba.id).all():
                            if evaluacion.alumno.curso == curso:
                                cant_evaluciones = cant_evaluciones +1
                                promedio = evaluacion.puntaje + promedio
                                banderaEvaluacionesCurso = True
                        if cant_evaluciones >0:
                            promedio = promedio / cant_evaluciones
                        promedio_taller = promedio_taller + promedio
                        if banderaEvaluacionesCurso:
                            cantidad_taller_con_evaluaciones = cantidad_taller_con_evaluaciones + 1
                if cantidad_taller_con_evaluaciones:
                    promedio_taller = int(promedio_taller/cantidad_taller_con_evaluaciones)
                data_taller.append(promedio_taller)

                promedio_tarea = 0
                cantidad_tareas_con_evaluaciones = 0
                for prueba in Prueba.objects(asignatura=asignatura.id, tipo="TAREA").all():
                    evaluaciones = Evaluacion.objects(prueba=prueba.id).all()
                    if evaluaciones:
                        promedio = 0
                        cant_evaluciones = 0
                        banderaEvaluacionesCurso = False
                        for evaluacion in Evaluacion.objects(prueba=prueba.id).all():
                            if evaluacion.alumno.curso == curso:
                                promedio = evaluacion.puntaje + promedio
                                cant_evaluciones = cant_evaluciones+1
                                banderaEvaluacionesCurso = True
                        if cant_evaluciones>0:
                            promedio = promedio / cant_evaluciones
                        promedio_tarea = promedio_tarea + promedio
                        if banderaEvaluacionesCurso:
                            cantidad_tareas_con_evaluaciones = cantidad_tareas_con_evaluaciones + 1
                if cantidad_tareas_con_evaluaciones:
                    promedio_tarea = int(promedio_tarea/cantidad_tareas_con_evaluaciones)
                data_tarea.append(promedio_tarea)


        return {"labels":labels,
                "data": [
                    {"data": data_ensayo, "label": "Ensayos"},
                    {"data": data_taller, "label": "Talleres"},
                    {"data": data_tarea, "label": "Tareas"},
                ]}


class AsignaturaToken(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AsignaturaToken, self).__init__()
    
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return Asignatura.objects(id=profesor.asignatura.id).first().to_dict()

    
class AsignaturasCurso(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AsignaturasCurso, self).__init__()

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
        curso = Curso.objects(id=id).first()
        for asignatura in curso.asignaturas:
            response.append(asignatura.to_dict())
        return response

class AsignaturaItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(AsignaturaItem, self).__init__()
    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        return Asignatura.objects(id=id).first().to_dict()
    
    def delete(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        asignatura = Asignatura.objects(id=id).first()
        asignatura.activo = False
        asignatura.save()
        return {'Response':'exito'}


class Asignaturas(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(Asignaturas, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        asignaturas = []
        if administrador != None or profesor != None:
            for asignatura in Asignatura.objects().all():
                if asignatura.activo:
                    asignaturas.append(asignatura.to_dict())
        if alumno != None:
            for asignatura in alumno.curso.asignaturas:
                if asignatura.activo:
                    asignaturas.append(asignatura.to_dict())
        if apoderado != None:
            for asignatura in apoderado.alumno.curso.asignaturas:
                if asignatura.activo:
                    asignaturas.append(asignatura.to_dict())
        return asignaturas

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
        asignatura = Asignatura()
        asignatura.nombre = data['nombre']
        asignatura.save()
        return {'Response': 'exito'}