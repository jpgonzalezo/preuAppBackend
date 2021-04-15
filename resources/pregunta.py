from flask import Flask, Blueprint, jsonify, request, send_file
from models.pregunta import Pregunta
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from flask_restful import reqparse
import os

def init_module(api):
    api.add_resource(PreguntaExcel, '/preguntaExcel')

class PreguntaExcel(Resource):
    def get(self):
        return Pregunta.create_layout_excel()