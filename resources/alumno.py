from flask import Flask, Blueprint, jsonify, request
from models.alumno import Alumno
from models.direccion import Direccion
from models.colegio import Colegio
from models.apoderado import Apoderado
from models.curso import Curso
from models.evaluacion import Evaluacion
from models.prueba import Prueba
from models.asignatura import Asignatura
from models.asistencia import Asistencia
from models.observacion import Observacion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util

def init_module(api):
    api.add_resource(AlumnoItem, '/alumno/<id>')
    api.add_resource(Alumnos, '/alumnos')
    api.add_resource(AlumnoHojaVida, '/hoja_vida/<id>')

class AlumnoHojaVida(Resource):
    def get(self,id):
        alumno = Alumno.objects(id=id).first()
        evaluaciones = Evaluacion.objects(alumno=alumno).all()
        evaluaciones_matematicas = []
        evaluaciones_lenguaje = []
        ponderacion_matematicas = 0
        ponderacion_lenguaje = 0
        colegio = ""
        if alumno.colegio!= None:
            colegio = alumno.colegio.nombre
        for evaluacion in evaluaciones:
            if (evaluacion.prueba.asignatura.nombre == 'Matemáticas') and (evaluacion.prueba.tipo != "TAREA"):
                evaluaciones_matematicas.append(evaluacion)

            if (evaluacion.prueba.asignatura.nombre == 'Lenguaje') and (evaluacion.prueba.tipo != "TAREA"):
                evaluaciones_lenguaje.append(evaluacion)
        
        for evaluacion_mat in evaluaciones_matematicas:
            ponderacion_matematicas = ponderacion_matematicas + evaluacion_mat.puntaje

        for evaluacion_leng in evaluaciones_lenguaje:
            ponderacion_lenguaje = ponderacion_lenguaje + evaluacion_leng.puntaje

        promedio_mat = 0
        promedio_leng = 0

        if ponderacion_matematicas>0:
            promedio_mat = int((ponderacion_matematicas)/evaluaciones_matematicas.__len__())
        
        if ponderacion_lenguaje>0:
            promedio_leng = int((ponderacion_lenguaje)/evaluaciones_lenguaje.__len__())
        
        asistencias = Asistencia.objects().all()
        cantidad_presente = 0
        for asistencia in asistencias:
            for alumno_presente in asistencia.alumnos_presentes:
                if alumno_presente.id == alumno.id:
                    cantidad_presente = cantidad_presente + 1
        
        promedio_asistencia = 0
        if cantidad_presente>0:
            promedio_asistencia = int(100*(cantidad_presente/asistencias.__len__()))

        observaciones = json.loads(Observacion.objects(alumno = alumno).all().to_json())

        return {
            'id': str(alumno.id),
            'nombres' : alumno.nombres,
            'calegio' : colegio,
            'curso' : alumno.curso.nombre,
            'apellido_paterno' : alumno.apellido_paterno,
            'apellido_materno' : alumno.apellido_materno,
            'telefono' : alumno.telefono,
            'email' : alumno.email,
            'ponderacion_matematicas' : promedio_mat,
            'ponderacion_lenguaje' : promedio_leng,
            'ponderacion_asistencia' : promedio_asistencia,
            'observaciones' : observaciones
        }

class AlumnoItem(Resource):
    def get(self, id):
        return json.loads(Alumno.objects(id=id).first().to_json())
        
    def delete(self, id):
        alumno = Alumno.objects(id=id).first()
        alumno.delete()
        return{'Response':'borrado'}


class Alumnos(Resource):
    def get(self):
        return json.loads(Alumno.objects().all().to_json())

    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        data_personal = data['data_personal']
        data_academico = data['data_academico']
        data_contacto = data['data_contacto']

        alumno = Alumno()
        alumno.nombres = data_personal['nombres']
        alumno.apellido_paterno = data_personal['apellido_paterno']
        alumno.apellido_materno = data_personal['apellido_materno']
        alumno.telefono = data_contacto['telefono']
        alumno.email = data_contacto['email']
        alumno.nombre_usuario = data_personal['nombre_usuario']
        alumno.password = data_personal['rut']
        alumno.sexo = data_personal['sexo']
        alumno.rut = data_personal['rut']
        alumno.puntaje_ingreso = data_academico['puntaje_ingreso']
        direccion = Direccion(calle=data_contacto['calle'],
                              numero=data_contacto['numero'],
                              comuna=data_contacto['comuna'])
        alumno.direccion = direccion
        colegio = Colegio.objects(id=data_academico['colegio']).first()
        curso = Curso.objects(id=data_academico['curso']).first()
        alumno.colegio = colegio
        alumno.curso = curso
        alumno.save()
        return {'Response': 'exito', 
                'nombres':data_personal['nombres'], 
                'apellido_paterno':data_personal['apellido_paterno'], 
                'apellido_materno':data_personal['apellido_materno']}