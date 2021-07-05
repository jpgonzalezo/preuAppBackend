from flask import Flask, Blueprint, jsonify, request, send_file
from models.pregunta import Pregunta
from models.prueba import Prueba
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from utils.excel_util import sheet_Tupla as excel_read
from flask_restful import reqparse
import os
from models.profesor import Profesor

def init_module(api):
    api.add_resource(PreguntaExcel, '/preguntaExcel/<id_prueba>')

class PreguntaExcel(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PreguntaExcel, self).__init__()
    def get(self,id_prueba):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        prueba = Prueba.objects(id=id_prueba).first()
        if profesor == None or prueba == None:
           return {'response': 'user_invalid'},401
        return Pregunta.create_layout_excel(prueba.topicos)

    def post(self):
        file = request.files["file"]
        lista = excel_read(file)
        #TODO: cambiar ese id por el que vendrá en el token
        return {'Response': Pregunta.create_from_excel(lista)}