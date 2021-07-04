from flask import Flask, Blueprint, jsonify, request
from models.prueba import Prueba
from models.pregunta import Pregunta
from models.asignatura import Asignatura
from models.curso import Curso
from models.evaluacion import Evaluacion
from models.administrador import Administrador
from models.apoderado import Apoderado
from models.respuesta import Respuesta
from models.alumno import Alumno
from models.profesor import Profesor
from models.topico import Topico
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from flask_restful import reqparse
from utils.excel_util import sheet_Tupla as excel_read

def init_module(api):
    api.add_resource(PruebaItem, '/pruebas/<id>')
    api.add_resource(PruebaTopico, '/pruebas/<id>/topico')
    api.add_resource(PruebaPregunta, '/pruebas/<id>/pregunta')
    api.add_resource(PruebaPreguntaNumero, '/pruebas/<id>/pregunta/<numero>')
    api.add_resource(PruebaPreguntaSubir, '/pruebas/<id>/pregunta/subir')
    api.add_resource(PruebaPreguntaBajar, '/pruebas/<id>/pregunta/bajar')
    api.add_resource(PruebaPreguntasExcel, '/pruebas/preguntasExcel')
    api.add_resource(Pruebas, '/pruebas')
    api.add_resource(PruebasAsignatura, '/pruebas_asignatura/<id>')
    api.add_resource(PruebaPuntajeBase, '/pruebas/<id>/asignar/puntaje/base')
    api.add_resource(PruebasAsignaturaToken, '/pruebas/asignatura')
    api.add_resource(PruebaRegistrarEvaluaciones, '/pruebas/<id>/registrar/evaluaciones')
    api.add_resource(GraficoRendimientoPreguntas, '/grafico/rendimiento/preguntas/<id>')
    api.add_resource(GraficoRendimientoTopicos, '/grafico/rendimiento/topicos/<id>')
    api.add_resource(GraficoRendimientoCursos, '/grafico/rendimiento/cursos/<id>')

def takeNumero(elem):
    return elem.numero_pregunta

class PruebaRegistrarEvaluaciones(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PruebaRegistrarEvaluaciones, self).__init__()
    #TODO:revisar logica
    def post(self,id):  
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        data = request.data.decode()
        data = json.loads(data)
        prueba = Prueba.objects(id=id).first()
        for registro in data['data']:
            evaluacion = Evaluacion()
            cantidad_buenas = 0
            cantidad_malas = 0
            cantidad_omitidas = 0
            alumno = Alumno.objects(id=registro['id']).first()
            evaluacion.alumno = alumno
            evaluacion.prueba = prueba
            for pregunta in prueba.preguntas:
                respuesta = Respuesta()
                respuesta.numero_pregunta = pregunta.numero_pregunta
                if registro[str(pregunta.numero_pregunta)] == "":
                    cantidad_omitidas = cantidad_omitidas + 1
                    respuesta.correcta = False
                    if prueba.tipo != "TAREA":
                        respuesta.alternativa = "O"
                else:
                    if prueba.tipo != "TAREA":
                        if registro[str(pregunta.numero_pregunta)].upper() == pregunta.alternativa.upper():
                            cantidad_buenas = cantidad_buenas + 1
                            respuesta.correcta = True
                            respuesta.alternativa = str(registro[str(pregunta.numero_pregunta)].upper())
                        else:
                            cantidad_malas = cantidad_malas + 1
                            respuesta.correcta = False
                            respuesta.alternativa = str(registro[str(pregunta.numero_pregunta)].upper())
                    else:
                        if registro[str(pregunta.numero_pregunta)].upper() == "CORRECTA":
                            cantidad_buenas = cantidad_buenas + 1
                            respuesta.correcta = True

                        if registro[str(pregunta.numero_pregunta)].upper() == "INCORRECTA":
                            cantidad_malas = cantidad_malas + 1
                            respuesta.correcta = False
                evaluacion.respuestas.append(respuesta)
            evaluacion.cantidad_buenas = cantidad_buenas
            evaluacion.cantidad_malas = cantidad_malas
            evaluacion.cantidad_omitidas = cantidad_omitidas
            evaluacion.puntaje = int(((850 - prueba.puntaje_base)/len(prueba.preguntas))*cantidad_buenas + prueba.puntaje_base)
            evaluacion.save()
        return {'Response':'exito'}
    
class PruebaPuntajeBase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PruebaPuntajeBase, self).__init__() 

    def put(self,id):  
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        data = request.data.decode()
        data = json.loads(data)
        if profesor == None:
            return {'response': 'user_invalid'},401
        data = request.data.decode()
        data = json.loads(data)
        prueba = Prueba.objects(id=id).first()
        prueba.puntaje_base = int(data['puntaje_base'])
        prueba.save()
        return {'Response':'exito'}

class PruebaPreguntaBajar(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PruebaPreguntaBajar, self).__init__()
        
    def post(self,id):  
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        data = request.data.decode()
        data = json.loads(data)
        if profesor == None:
            return {'response': 'user_invalid'},401
        data = request.data.decode()
        data = json.loads(data)
        prueba = Prueba.objects(id=id).first()
        for pregunta in prueba.preguntas:
            if int(pregunta.numero_pregunta) == int(data['numero']):
                pregunta.numero_pregunta = pregunta.numero_pregunta + 1
            else:
                if int(pregunta.numero_pregunta) == int(data['numero'])+1:
                    pregunta.numero_pregunta = pregunta.numero_pregunta - 1
        prueba.preguntas.sort(key=takeNumero)
        prueba.save()
        return {'Response':'exito'}

class PruebaPreguntaSubir(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PruebaPreguntaSubir, self).__init__()

    def post(self,id):  
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        data = request.data.decode()
        data = json.loads(data)
        if profesor == None:
            return {'response': 'user_invalid'},401
        data = request.data.decode()
        data = json.loads(data)
        prueba = Prueba.objects(id=id).first()
        for pregunta in prueba.preguntas:
            if int(pregunta.numero_pregunta) == int(data['numero']):
                pregunta.numero_pregunta = pregunta.numero_pregunta - 1
            else:
                if int(pregunta.numero_pregunta) == int(data['numero'])-1:
                    pregunta.numero_pregunta = pregunta.numero_pregunta + 1
        prueba.preguntas.sort(key=takeNumero)
        prueba.save()
        return {'Response':'exito'}
    
class PruebaPreguntaNumero(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PruebaPreguntaNumero, self).__init__()

    def delete(self,id,numero):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        if profesor == None:
            return {'response': 'user_invalid'},401
        prueba = Prueba.objects(id=id).first()
        preguntas = []
        for pregunta in prueba.preguntas:
            if pregunta.numero_pregunta != int(numero):
                preguntas.append(pregunta)
        contador = 0
        for pregunta in preguntas:
            pregunta.numero_pregunta = contador + 1
            contador = contador + 1
        prueba.preguntas = preguntas
        prueba.save()
        return {"Response":"borrado"}

class PruebaPregunta(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PruebaPregunta, self).__init__()

    def post(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        data = request.data.decode()
        data = json.loads(data)
        if profesor == None:
            return {'response': 'user_invalid'},401
        data = request.data.decode()
        data = json.loads(data)
        prueba = Prueba.objects(id=id).first()
        topico = Topico.objects(id=data['topico']).first()
        pregunta = Pregunta()
        if(data['tipo']=="TAREA"):
            pregunta.numero_pregunta = len(prueba.preguntas)+1
            pregunta.topico = topico
        else:
            pregunta.numero_pregunta = len(prueba.preguntas)+1
            pregunta.topico = topico
            pregunta.alternativa = data['alternativa']
        prueba.preguntas.append(pregunta)
        prueba.cantidad_preguntas = len(prueba.preguntas)
        prueba.save()
        return {"Response":"exito"}

class PruebaTopico(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PruebaTopico, self).__init__()

    
    def put(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        data = request.data.decode()
        data = json.loads(data)
        if profesor == None:
            return {'response': 'user_invalid'},401
        data = request.data.decode()
        data = json.loads(data)
        prueba = Prueba.objects(id=id).first()
        topico = Topico.objects(id=data['id']).first()
        prueba.topicos.append(topico.id)
        prueba.save()
        return {"Response":"exito"}


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
                        cantidad = int(cantidad_correctas)
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
                        cantidad = int(cantidad_correctas)
                    data_curso.append(cantidad)
                data.append({
                    "data": data_curso,
                    "label": curso.nombre
                })
                
        return{
            "labels":labels,
            "data": data
        }

class PruebasAsignaturaToken(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PruebasAsignaturaToken, self).__init__()
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
        asignatura = Asignatura.objects(id=profesor.asignatura.id).first()
        for prueba in Prueba.objects(asignatura=asignatura.id ,activo=True):
            response.append(prueba.to_dict())
        return response
    
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
        for prueba in Prueba.objects(asignatura=asignatura.id,activo=True):
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
    
    def delete(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        if profesor == None:
            return {'response': 'user_invalid'},401
        prueba = Prueba.objects(id=id).first()
        prueba.activo = False
        prueba.save()
        return {'Response':'borrado'}

    def put(self,id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        if profesor == None:
            return {'response': 'user_invalid'},401
        return {'Response':Prueba.update_visible(id)}

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
    def post(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        data = request.data.decode()
        data = json.loads(data)
        if profesor == None:
            return {'response': 'user_invalid'},401
        prueba = Prueba()
        prueba.nombre = data['nombre']
        prueba.cantidad_preguntas = 0
        prueba.asignatura = profesor.asignatura.id
        prueba.tipo = data['tipo']
        prueba.save()
        return {"Response":"exito", 'id':str(prueba.id)}

class PruebaPreguntasExcel(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        self.reqparse.add_argument('prueba_id',type=str,required=True,location='args')
        super(PruebaPreguntasExcel, self).__init__()

    def post(self):
        file = request.files["file"]
        lista = excel_read(file)
        args = self.reqparse.parse_args()
        prueba_id = args.get('prueba_id')
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        if profesor == None:
           return {'response': 'user_invalid'},401
        return Prueba.load_preguntas(lista, prueba_id)
