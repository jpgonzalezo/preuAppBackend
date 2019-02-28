from flask import Flask, redirect, url_for, request, render_template, jsonify, current_app
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.base import MenuLink
from libs.model_view import ModelView
from db import db
from flask_babelex import Babel

from models.curso import Curso
from models.colegio import Colegio
from models.asignatura import Asignatura
from models.profesor import Profesor
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.evaluacion import Evaluacion
from models.administrador import Administrador
from models.region import Region
from models.ciudad import Ciudad 
from models.comuna import Comuna
from models.topico import Topico
from models.prueba import Prueba
from models.alerta import Alerta
from models.observacion import Observacion
from models.asistencia import Asistencia
from models.justificacion import Justificacion

def create_app(config="config.cfg"):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    babel = Babel(app)
    db.init_app(app)
    admin = Admin(app, name='PreuApp', template_mode='bootstrap3')
    @babel.localeselector
    def get_locale():
        return "es"

    return app, admin


def add_views(admin):
    
    admin.add_view(ModelView(Curso, "Cursos", category="Curso"))
    admin.add_view(ModelView(Asignatura, "Asignaturas", category="Curso"))

    admin.add_view(ModelView(Administrador, "Administradores de Institucion", category="Perfiles"))
    admin.add_view(ModelView(Profesor, "Profesores", category="Perfiles"))
    admin.add_view(ModelView(Alumno, "Alumnos", category="Perfiles"))
    admin.add_view(ModelView(Apoderado, "Apoderados", category="Perfiles"))
    
    admin.add_view(ModelView(Evaluacion, "Evaluaciones Realizadas", category="Evaluacion"))
    admin.add_view(ModelView(Topico, "Topicos", category="Evaluacion"))
    admin.add_view(ModelView(Prueba, "Pruebas", category="Evaluacion"))
    
    admin.add_view(ModelView(Colegio, "Colegios"))
    admin.add_view(ModelView(Alerta, "Alertas"))
    admin.add_view(ModelView(Observacion, "Observaciones"))

    admin.add_view(ModelView(Ciudad, "Ciudades",category="Direccion"))
    admin.add_view(ModelView(Region, "Regiones",category="Direccion"))
    admin.add_view(ModelView(Comuna, "Comunas",category="Direccion"))

    admin.add_view(ModelView(Asistencia, "Asistencias", category="Asistencia y justificaciones"))
    admin.add_view(ModelView(Justificacion, "Justificaciones", category="Asistencia y justificaciones"))

app, admin = create_app()
add_views(admin)

if __name__ == '__main__':
    app.run(host=app.config.get('HOST', '0.0.0.0'),
            port=app.config.get('PORT', 4000))