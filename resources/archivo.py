from flask import Flask, Blueprint, jsonify, request, current_app
from models.alumno import Alumno
from models.archivo import Archivo
from models.administrador import Administrador
from models.apoderado import Apoderado
from models.profesor import Profesor
from models.asignatura import Asignatura
from models.evaluacion import Evaluacion
from utils.excel_util import sheet_Tupla as excel
from utils.excel_util import create_workbook as create
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from datetime import datetime, date, time, timedelta
import calendar
from flask_restful import reqparse

def init_module(api):
    api.add_resource(ArchivoAsignatura, '/archivoAsignatura/<asignatura_id>')
    api.add_resource(ArchivoItem, '/archivos','/archivo/<archivo_id>')
    api.add_resource(ArchivoEnExcel, '/archivoExcel')



class ArchivoAsignatura(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ArchivoAsignatura, self).__init__()

    def post(self,asignatura_id):
        file = request.files["file"]
        return {'Response': Archivo.upload(current_app.config.get("BASE_PATH"), file , asignatura_id)}

    def get(self, asignatura_id):
        return Archivo.get_all_by_asignatura(asignatura_id)

class ArchivoItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ArchivoItem, self).__init__()

    def get(self,archivo_id = None):
        if archivo_id:
            return Archivo.download(archivo_id)
        else:
            return Archivo.get_all()
    
    def delete(self, archivo_id):
        
        return {'Response': Archivo.erase(archivo_id)}

class ArchivoEnExcel(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(ArchivoEnExcel, self).__init__()

    def post(self):
        file = request.files["file"]
        print (excel(file))
        return excel(file)

    def get(self):
        return create( {'A': '"Dog,Cat,Bat"', 'C': '"wea1, wea2, wea3"'}, 100, ['Animal','  ', "WEA"])


