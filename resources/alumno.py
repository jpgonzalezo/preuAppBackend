from flask import Flask, Blueprint, jsonify, request, send_file
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
from models.prueba import Prueba
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from PIL import Image
import os

def init_module(api):
    api.add_resource(AlumnoItem, '/alumno/<id>')
    api.add_resource(Alumnos, '/alumnos')
    api.add_resource(AlumnoHojaVida, '/hoja_vida/<id>')
    api.add_resource(AlumnoImagenItem, '/alumno_imagen/<id>')
    api.add_resource(AlumnoImagenDefault, '/alumno_imagen_default/<id>')
    api.add_resource(AlumnosCurso, '/alumnos_curso/<id_curso>')
    api.add_resource(AlumnoGraficoRendimiento, '/alumno_grafico_rendimiento/<id>')
    api.add_resource(AlumnoGraficoAsistencia, '/alumno_grafico_asistencia/<id>')

class AlumnoGraficoAsistencia(Resource):
    def get(self,id):
        labels = []
        data_asistencia_asignatura = []
        data_inasistencia_asignatura = []
        data_asistencia_anual = []
        data_inasistencia_anual = []
        labels_anual = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
        meses = [1,2,3,4,5,6,7,8,9,10,11,12]
        alumno = Alumno.objects(id=id).first()
        for asignatura in alumno.curso.asignaturas:
            labels.append(asignatura.nombre)
            presentes = 0
            for asistencia in Asistencia.objects(asignatura=asignatura).all():  
                if alumno in asistencia.alumnos_presentes:
                    presentes = presentes + 1
            if Asistencia.objects(asignatura=asignatura).count()>0:
                presentes = int((presentes/Asistencia.objects(asignatura=asignatura).count())*100)
            data_asistencia_asignatura.append(presentes)
            data_inasistencia_asignatura.append(100-presentes)
        
        for mes in meses:
            asistencia_mes = 0
            cant_asistencia = 0
            aprobacion = 0
            for asistencia in Asistencia.objects(curso = alumno.curso).all():
                if str(asistencia.fecha.month) == str(mes):
                    cant_asistencia = cant_asistencia + 1
                    if alumno in asistencia.alumnos_presentes:
                        asistencia_mes = asistencia_mes + 1
            if cant_asistencia> 0:
                aprobacion = int((asistencia_mes/cant_asistencia)*100)
            data_asistencia_anual.append(aprobacion)
            data_inasistencia_anual.append(100-aprobacion)

        return {
            "grafico_asignatura" : {
                "labels" : labels,
                "data": [
                    {"data":data_inasistencia_asignatura, "label":"Inasistencia"},
                    {"data":data_asistencia_asignatura, "label":"Asistencia"}
                ]
            },
            "grafico_anual":{
                "labels": labels_anual,
                "data": [
                    {"data":data_inasistencia_anual, "label":"Inasistencia"},
                    {"data":data_asistencia_anual, "label":"Asistencia"}
                ]
            }
        }
class AlumnoGraficoRendimiento(Resource):
    def get(self,id):
        labels=[]
        data_ensayo = []
        data_taller = []
        data_tarea = []
        alumno = Alumno.objects(id=id).first()
        for asignatura in alumno.curso.asignaturas:
            labels.append(asignatura.nombre)
            suma_ensayo = 0
            suma_taller = 0
            suma_tarea = 0
            for prueba in Prueba.objects(asignatura = asignatura, tipo ="ENSAYO").all():
                puntaje = 0
                evaluacion = Evaluacion.objects(alumno=alumno.id, prueba=prueba.id).first()
                if evaluacion != None:
                    puntaje = evaluacion.puntaje
                suma_ensayo = suma_ensayo + puntaje
            
            for prueba in Prueba.objects(asignatura = asignatura, tipo ="TALLER").all():
                puntaje = 0
                evaluacion = Evaluacion.objects(alumno=alumno.id, prueba=prueba.id).first()
                if evaluacion != None:
                    puntaje = evaluacion.puntaje
                suma_taller = suma_taller + puntaje
            
            for prueba in Prueba.objects(asignatura = asignatura, tipo ="TAREA").all():
                puntaje = 0
                evaluacion = Evaluacion.objects(alumno=alumno.id, prueba=prueba.id).first()
                if evaluacion != None:
                    puntaje = evaluacion.puntaje
                suma_tarea = suma_tarea + puntaje

            if Prueba.objects(asignatura = asignatura, tipo ="ENSAYO").count()>0:
                data_ensayo.append((suma_ensayo/Prueba.objects(asignatura = asignatura, tipo ="ENSAYO").count()))
            if Prueba.objects(asignatura = asignatura, tipo ="ENSAYO").count()==0:
                data_ensayo.append(suma_ensayo)


            if Prueba.objects(asignatura = asignatura, tipo ="TALLER").count()>0:
                data_taller.append((suma_taller/Prueba.objects(asignatura = asignatura, tipo ="TALLER").count()))
            if Prueba.objects(asignatura = asignatura, tipo ="TALLER").count()==0:
                data_taller.append(suma_taller)


            if Prueba.objects(asignatura = asignatura, tipo ="TAREA").count()>0:
                data_tarea.append((suma_tarea/Prueba.objects(asignatura = asignatura, tipo ="TAREA").count()))
            if Prueba.objects(asignatura = asignatura, tipo ="TAREA").count()==0:
                data_tarea.append(suma_tarea)


        return{
            "labels": labels,
            "data": [
                {"data": data_ensayo , "label":"Ensayo"},
                {"data": data_taller , "label":"Taller"},
                {"data": data_tarea , "label":"Tarea"}
            ]
        }
class AlumnosCurso(Resource):
    def get(self,id_curso):
        alumnos = []
        curso = Curso.objects(id=id_curso).first()
        for alumno in Alumno.objects(curso = curso.id).all():
            if alumno.activo:
                alumnos.append(alumno.to_dict())
        return alumnos
class AlumnoHojaVida(Resource):
    def get(self,id):
        alumno = Alumno.objects(id=id).first()
        evaluaciones = Evaluacion.objects(alumno=alumno.id).all()
        print(evaluaciones)
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
            'observaciones' : observaciones,
            'imagen': alumno.imagen
        }

class AlumnoItem(Resource):
    def get(self, id):
        return json.loads(Alumno.objects(id=id).first().to_json())
        
    def delete(self, id):
        alumno = Alumno.objects(id=id).first()
        alumno.activo = False
        alumno.save()
        colegio = Colegio.objects(id= alumno.colegio.id).first()
        curso = Curso.objects(id= alumno.curso.id).first()
        colegio.updateCantEstudiantes()
        curso.updateCantEstudiantes()
        colegio.save()
        curso.save()
        return{'Response':'borrado'}


class Alumnos(Resource):
    def get(self):
        response = []
        alumnos = Alumno.objects().all()
        for alumno in alumnos:
            if alumno.activo:
                response.append(alumno.to_dict())
        return response
    

    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        alumno = Alumno()
        alumno.nombres = data['nombres']
        alumno.apellido_paterno = data['apellido_paterno']
        alumno.apellido_materno = data['apellido_materno']
        alumno.telefono = data['telefono']
        alumno.email = data['email']
        alumno.password = data['rut']
        alumno.sexo = data['sexo']
        alumno.rut = data['rut']
        alumno.puntaje_ingreso = data['puntaje_ingreso']
        direccion = Direccion(calle=data['calle'],
                              numero=data['numero'],
                              comuna=data['comuna'])
        alumno.direccion = direccion
        colegio = Colegio.objects(id=data['colegio']).first()
        curso = Curso.objects(id=data['curso']).first()
        alumno.colegio = colegio
        alumno.curso = curso
        alumno.save()
        colegio.updateCantEstudiantes()
        curso.updateCantEstudiantes()
        colegio.save()
        curso.save()
        return {'Response': 'exito',
                'id': str(alumno.id)}

class AlumnoImagenItem(Resource):
    def post(self,id):
        imagen = Image.open(request.files['imagen'].stream).convert("RGB")
        imagen.save(os.path.join("./uploads/alumnos", str(id)+".jpg"))
        imagen.thumbnail((800, 800))
        imagen.save(os.path.join("./uploads/alumnos", str(id)+'_thumbnail.jpg'))
        alumno = Alumno.objects(id=id).first()
        alumno.imagen = id
        alumno.save()
        return {'Response': 'exito'}
    
    def get(self,id):
        return send_file('uploads/alumnos/'+id+'_thumbnail.jpg')

class AlumnoImagenDefault(Resource):
    def get(self,id):
        alumno = Alumno.objects(id=id).first()
        alumno.imagen = "default"
        alumno.save()
        return { 'Response':'exito'}