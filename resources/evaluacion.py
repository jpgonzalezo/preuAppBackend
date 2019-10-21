from flask import Flask, Blueprint, jsonify, request
from models.prueba import Prueba
from models.evaluacion import Evaluacion
from models.administrador import Administrador
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.profesor import Profesor
from models.curso import Curso
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from flask_restful import reqparse

def init_module(api):
    api.add_resource(EvaluacionesPrueba, '/evaluaciones/prueba/<id>')
    api.add_resource(EvaluacionPruebaRegistroColumnas, '/evaluaciones/prueba/<id_prueba>/registrar/columnas')
    api.add_resource(EvaluacionRegistroFilas, '/evaluaciones/<id_evaluacion>/editar/registro/filas')
    api.add_resource(EvaluacionRegistroAlternativas, '/evaluaciones/<id_evaluacion>/editar/alternativas')
    api.add_resource(EvaluacionPruebaRegistro, '/evaluaciones/prueba/<id_prueba>/curso/<id_curso>/registrar')
    api.add_resource(EvaluacionItem, '/evaluaciones/<id_evaluacion>')
    api.add_resource(EvaluacionPuntaje, '/evaluaciones/<id_evaluacion>/puntaje')

class EvaluacionRegistroAlternativas(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(EvaluacionRegistroAlternativas, self).__init__()

    def post(self,id_evaluacion):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        data = request.data.decode()
        data = json.loads(data)
        evaluacion = Evaluacion.objects(id=id_evaluacion).first()
        cantidad_buenas = 0
        cantidad_malas = 0
        cantidad_omitidas = 0
        for respuesta in evaluacion.respuestas:
            for registro in data['data']:
                if registro[str(respuesta.numero_pregunta)].upper() == respuesta.alternativa.upper():
                    for pregunta in evaluacion.prueba.preguntas:
                        if pregunta.numero_pregunta == respuesta.numero_pregunta:
                            if respuesta.alternativa == "":
                                cantidad_omitidas = cantidad_omitidas + 1
                            else:
                                if pregunta.alternativa.upper() == respuesta.alternativa.upper():
                                    cantidad_buenas = cantidad_buenas + 1
                                else:
                                    cantidad_malas = cantidad_malas + 1
                else:
                    if str(registro[str(respuesta.numero_pregunta)].upper()) == "" or str(registro[str(respuesta.numero_pregunta)].upper()) == "O":
                        respuesta.alternativa = "O"
                    else:
                        respuesta.alternativa = str(registro[str(respuesta.numero_pregunta)].upper())
                    for pregunta in evaluacion.prueba.preguntas:
                        if pregunta.numero_pregunta == respuesta.numero_pregunta:
                            if respuesta.alternativa == "" or respuesta.alternativa == "O":
                                cantidad_omitidas = cantidad_omitidas + 1
                            else:
                                if pregunta.alternativa.upper() == respuesta.alternativa.upper():
                                    respuesta.correcta = True
                                    cantidad_buenas = cantidad_buenas + 1
                                else:
                                    respuesta.correcta = False
                                    cantidad_malas = cantidad_malas + 1
        
        evaluacion.cantidad_buenas = cantidad_buenas
        evaluacion.cantidad_malas = cantidad_malas
        evaluacion.cantidad_omitidas = cantidad_omitidas
        puntaje_base = evaluacion.prueba.puntaje_base
        if puntaje_base == 0:
            evaluacion.puntaje = int((850/len(evaluacion.prueba.preguntas))*cantidad_buenas)
        else:
            evaluacion.puntaje = int(((850-puntaje_base)/len(evaluacion.prueba.preguntas))*cantidad_buenas + puntaje_base)
        evaluacion.save()
        return {'Response':'exito'}

class EvaluacionRegistroFilas(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(EvaluacionRegistroFilas, self).__init__()
    
    def get(self,id_evaluacion):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        evaluacion = Evaluacion.objects(id=id_evaluacion).first()
        rowsData = []
        rowsData.append({ 'id':str(evaluacion.alumno.id),'nombres': evaluacion.alumno.nombres, 'apellido_paterno': evaluacion.alumno.apellido_paterno, 'apellido_materno': evaluacion.alumno.apellido_materno})
        for row in rowsData:
            for respuesta in evaluacion.respuestas:
                if respuesta.alternativa == "O":
                    row[str(respuesta.numero_pregunta)] = ""
                else:
                    row[str(respuesta.numero_pregunta)] = respuesta.alternativa
        return rowsData

class EvaluacionPuntaje(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(EvaluacionPuntaje, self).__init__()
    
    def put(self,id_evaluacion):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        if profesor == None:
            return {'response': 'user_invalid'},401
        evaluacion = Evaluacion.objects(id=id_evaluacion).first()
        data = request.data.decode()
        data = json.loads(data)
        evaluacion.puntaje = int(data['puntaje'])
        evaluacion.save()
        return {'Response':'exito'},200

class EvaluacionItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(EvaluacionItem, self).__init__()
    def delete(self,id_evaluacion):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        evaluacion = Evaluacion.objects(id=id_evaluacion).first()
        if evaluacion !=None:
            evaluacion.delete()
        return {'Response':'borrado'}
    def get(self,id_evaluacion):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        evaluacion = Evaluacion.objects(id=id_evaluacion).first()
        return evaluacion.to_dict()



class EvaluacionPruebaRegistroColumnas(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(EvaluacionPruebaRegistroColumnas, self).__init__()
    def get(self,id_prueba):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        columnDefs = []
        columnDefs.append({'headerName':'Nombres','field':'nombres','sortable':True})
        columnDefs.append({'headerName':'Apellido Paterno','field':'apellido_paterno','sortable':True})
        columnDefs.append({'headerName':'Apellido Materno','field':'apellido_materno','sortable':True})
        prueba = Prueba.objects(id=id_prueba).first()
        for pregunta in prueba.preguntas:
            if prueba.tipo == "ENSAYO" or prueba.tipo == "TALLER":
                columnDefs.append({'headerName':str(pregunta.numero_pregunta),'field':str(pregunta.numero_pregunta),'editable':True,'width':40 })
            if prueba.tipo == "TAREA":
                columnDefs.append({'headerName':str(pregunta.numero_pregunta),'field':str(pregunta.numero_pregunta),'editable':True,'width':80, 'cellEditor': 'select',   'cellEditorParams': {'values': ['correcta','incorrecta']} } )
        return columnDefs


class EvaluacionPruebaRegistro(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(EvaluacionPruebaRegistro, self).__init__()
    def get(self,id_prueba,id_curso):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'},401
        rowsData = []
        prueba = Prueba.objects(id=id_prueba).first()
        curso = Curso.objects(id=id_curso).first()
        for alumno in Alumno.objects(curso=curso,activo=True).all():
            if Evaluacion.objects(prueba=prueba,alumno=alumno).first() == None:
                rowsData.append({ 'id':str(alumno.id),'nombres': alumno.nombres, 'apellido_paterno': alumno.apellido_paterno, 'apellido_materno': alumno.apellido_materno})
        for row in rowsData:
            for pregunta in prueba.preguntas:
                row[str(pregunta.numero_pregunta)] = ""
        return rowsData

class EvaluacionesPrueba(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(EvaluacionesPrueba, self).__init__()
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
        prueba = Prueba.objects(id=id).first()
        for evaluacion in Evaluacion.objects(prueba=prueba.id):
            response.append(evaluacion.to_dict())
        return response