from flask import Flask, redirect, url_for, request, render_template, jsonify, current_app
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.base import MenuLink
from libs.model_view import ModelView
from db import db
from flask_babelex import Babel
from models.curso import Curso
from models.institucion import Institucion
from models.asignatura import Asignatura
from models.profesor import Profesor
from models.alumno import Alumno
from models.evaluacion import Evaluacion
from models.inscripcion import Inscripcion
from models.administrador import Administrador
from models.portal import Portal

def create_app(config="config.cfg"):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    babel = Babel(app)
    db.init_app(app)
    admin = Admin(app, name='VR4kidz', template_mode='bootstrap3')
    @babel.localeselector
    def get_locale():
        return "es"

    return app, admin


def add_views(admin):
    
    admin.add_view(ModelView(Curso, "Cursos", category="Curso"))
    admin.add_view(ModelView(Asignatura, "Asignaturas", category="Curso"))
    admin.add_view(ModelView(Inscripcion, "Inscripciones", category="Curso"))

    admin.add_view(ModelView(Administrador, "Administradores de Institucion", category="Perfiles"))
    admin.add_view(ModelView(Profesor, "Profesores", category="Perfiles"))
    admin.add_view(ModelView(Alumno, "Alumnos", category="Perfiles"))
    
    
    admin.add_view(ModelView(Evaluacion, "Evaluaciones", category="Evaluacion"))
    
    admin.add_view(ModelView(Institucion, "Instituciones", category="Institucion"))
    admin.add_view(ModelView(Portal, "Portales",category="Institucion"))


app, admin = create_app()
add_views(admin)

if __name__ == '__main__':
    app.run(host=app.config.get('HOST', '0.0.0.0'),
            port=app.config.get('PORT', 4000))