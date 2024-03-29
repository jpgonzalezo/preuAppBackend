from flask import Flask, Blueprint
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from db import db
from mail import mail
from models.asignatura import Asignatura
import json

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
api_bp = Blueprint('api', __name__)
CORS(api_bp)
mail.init_app(app)
api = Api(api_bp)
app.register_blueprint(api_bp)



def init_modules(app, api):
    from resources import curso
    from resources import alumno
    from resources import login
    from resources import estadistica
    from resources import colegio
    from resources import apoderado
    from resources import observacion
    from resources import profesor
    from resources import asignatura
    from resources import asistencia
    from resources import administrador
    from resources import justificacion
    from resources import anotacion
    from resources import alerta
    from resources import prueba
    from resources import topico
    from resources import evaluacion
    from resources import evento
    from resources import archivo
    from resources import video
    from resources import pregunta


    curso.init_module(api)
    alumno.init_module(api)
    login.init_module(api)
    estadistica.init_module(api)
    colegio.init_module(api)
    apoderado.init_module(api)
    observacion.init_module(api)
    profesor.init_module(api)
    asignatura.init_module(api)
    asistencia.init_module(api)
    administrador.init_module(api)
    justificacion.init_module(api)
    anotacion.init_module(api)
    alerta.init_module(api)
    prueba.init_module(api)
    topico.init_module(api)
    evaluacion.init_module(api)
    evento.init_module(api)
    archivo.init_module(api)
    pregunta.init_module(api)
    video.init_module(api)

init_modules(app, api)

if __name__ == '__main__':
    app.run(host='0.0.0.0')