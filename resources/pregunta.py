from flask import Flask, Blueprint, jsonify, request, send_file
from models.pregunta import Pregunta
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from utils.excel_util import sheet_Tupla as excel_read
from flask_restful import reqparse
import os
from models.profesor import Profesor

def init_module(api):
    api.add_resource(PreguntaExcel, '/preguntaExcel')

class PreguntaExcel(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('auth-token', type = str, required=True, location='headers')
        super(PreguntaExcel, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        profesor = Profesor.load_from_token(token)
        #if profesor == None:
         #   return {'response': 'user_invalid'},401
        return Pregunta.create_layout_excel(profesor.asignatura.id)

    def post(self):
        file = request.files["file"]
        lista = excel_read(file)
        #TODO: cambiar ese id por el que vendrá en el token
        return {'Response': Pregunta.create_from_excel(lista,'6074bd2430d005137041a2b2')}