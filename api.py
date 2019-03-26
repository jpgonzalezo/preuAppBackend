from flask import Flask, Blueprint
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from db import db
from models.asignatura import Asignatura
import json

app = Flask(__name__)
CORS(app)
api_bp = Blueprint('api', __name__)
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

    curso.init_module(api)
    alumno.init_module(api)
    login.init_module(api)
    estadistica.init_module(api)
    colegio.init_module(api)
    apoderado.init_module(api)
    observacion.init_module(api)


init_modules(app, api)


if __name__ == '__main__':
    app.run(debug=True)