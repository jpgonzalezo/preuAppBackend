from flask import Flask, Blueprint, jsonify, request
from models.alumno import Alumno
from models.archivo import Archivo
from models.administrador import Administrador
from models.apoderado import Apoderado
from models.profesor import Profesor
from models.asignatura import Asignatura
from models.video import Video
from models.curso import Curso
from models.evaluacion import Evaluacion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from datetime import datetime, date, time, timedelta
import calendar
from flask_restful import reqparse


def init_module(api):
    api.add_resource(VideoCursoAsignatura, '/video')
    api.add_resource(VideoItem, '/video/<video_id>')



class VideoCursoAsignatura(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'auth-token', type=str, required=True, location='headers')
        super(VideoCursoAsignatura, self).__init__()

    def post(self):
        body = request.data.decode()
        body = json.loads(body)
        return Video.create(body)

    def get(self):
        asignatura_id = request.args.get('asignatura_id')
        curso_id = request.args.get('curso_id')
        return Video.get_all_by_asignatura_and_curso(asignatura_id, curso_id)


class VideoItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
        'auth-token', type=str, required=True, location='headers')
        super(VideoItem, self).__init__()

    def get(self, video_id):
        return Video.get_by_id(video_id)

    def delete(self, video_id):
        return {'Response': Video.erase(video_id)}
