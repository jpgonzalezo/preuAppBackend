from flask import Flask, redirect, url_for, request, render_template, jsonify, current_app
from flask_admin import Admin, AdminIndexView, expose, BaseView, expose
from flask_admin.base import MenuLink
from libs.model_view import ModelView
from db import db
from flask_babelex import Babel
from werkzeug.utils import secure_filename
import os
import xlrd
from models.curso import Curso
from models.colegio import Colegio
from models.asignatura import Asignatura
from models.profesor import Profesor
from models.alumno import Alumno
from models.apoderado import Apoderado
from models.evaluacion import Evaluacion
from models.administrador import Administrador
from models.direccion import Direccion
from models.region import Region
from models.ciudad import Ciudad 
from models.comuna import Comuna
from models.topico import Topico
from models.prueba import Prueba
from models.alerta import Alerta
from models.observacion import Observacion,ObservacionProfesor
from models.asistencia import Asistencia
from models.justificacion import Justificacion
from models.anotacion import Anotacion
from models.evento import Evento
from models.archivo import Archivo
from models.video import Video

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

app, admin = create_app()

class ViewWithMethodViews(BaseView):
    @expose('/', methods=["POST", "GET"])
    def index(self):
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                return "<h2>Debe enviar un archivo</h2>"
            file = request.files['file']
            if file.filename == '':
                return "<h2>Debe enviar un archivo</h2>"
            if not ".xls" in file.filename:
                return "<h2>El archivo debe ser un excel</h2>"
            if file:
                filename = secure_filename(file.filename)
                filename = filename
                filepath = os.path.join("/tmp", filename)
                file.save(filepath)
                url_path = url_for('.process_file', filename=filename)
            return "<a href='%s'><h2>Procesar excel</h2></a><hr><a href='%s'>otra funcion con la misma xls</a>" % (url_path, "falso")
            
        return """<title>Subir Excel</title>
                  <h3>Selecciona el archivo</h3>
                  <form method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <input type="submit" value="Subir archivo" class="btn btn-default">
                  </form>"""
    
    #Referencias filas excel
    # a b c d e f g h i j k  l  m  n  o  p  q  r  s  t  u  v  w  x  y  z  aa ab ac ad ae af ag
    # 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 
    @expose('/import/process/<filename>')
    def process_file(self, filename):
        from xlrd import open_workbook, xldate_as_tuple
        filas = 0
        filepath = os.path.join('/tmp', filename)
        wb = open_workbook(filepath)
        sheet = wb.sheets()[0]
        filas_importadas = 0
        for row in range(1, sheet.nrows):
            rut = str(sheet.cell(row, 0).value)
            if Alumno.objects(rut=rut).first() == None:
                nombres = str(sheet.cell(row, 1).value)
                apel_pa = str(sheet.cell(row, 2).value)
                apel_ma = str(sheet.cell(row, 3).value)
                sexo = str(sheet.cell(row, 4).value)
                email   = str(sheet.cell(row, 5).value)
                telefono = str(sheet.cell(row, 6).value)
                calle = str(sheet.cell(row, 7).value)
                numero = str(sheet.cell(row, 8).value)
                comuna = str(sheet.cell(row, 9).value)
                curso = str(sheet.cell(row, 10).value)
                colegio = str(sheet.cell(row, 11).value)
                colegio_calle = str(sheet.cell(row, 12).value)
                colegio_numero = str(sheet.cell(row, 13).value)
                colegio_comuna = str(sheet.cell(row, 14).value)
                alumno = Alumno()
                alumno.rut = rut
                alumno.encrypt_password(rut)
                alumno.nombres = nombres
                alumno.apellido_paterno = apel_pa
                alumno.apellido_materno = apel_ma
                if sexo == 'M':
                    alumno.sexo = 'MASCULINO'
                if sexo == 'F':
                    alumno.sexo = 'FEMENINO'
                if curso == 'C':
                    ciencias = Curso.objects(nombre="Ciencias 2019").first()
                    if ciencias != None:
                        alumno.curso = ciencias.id
                if curso == 'H':
                    historia = Curso.objects(nombre="Historia 2019").first()
                    if historia != None:
                        alumno.curso = historia.id
                alumno.email = email
                alumno.telefono = telefono
                direccion = Direccion()
                direccion.calle = calle
                direccion.numero = numero
                direccion.comuna = comuna
                alumno.direccion = direccion
                colegio_alumno = Colegio.objects(nombre = colegio).first()
                if colegio_alumno != None:
                    alumno.colegio = colegio_alumno.id
                else:
                    colegio_alumno = Colegio()
                    colegio_alumno.nombre = colegio
                    direccion = Direccion()
                    direccion.calle = colegio_calle
                    direccion.numero = colegio_numero
                    direccion.comuna = colegio_comuna
                    colegio_alumno.direccion = direccion
                    colegio_alumno.save()
                    alumno.colegio = colegio_alumno.id
                alumno.imagen = "default"
                alumno.puntaje_ingreso = 500
                alumno.save()
                filas_importadas += 1
        for colegio in Colegio.objects().all():
            colegio.updateCantEstudiantes()
        for curso in Curso.objects().all():
            curso.updateCantEstudiantes()
        return "%d Fila importadas" % filas_importadas


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
    admin.add_view(ModelView(Observacion, "Observaciones Alumnos",category="Observaciones"))
    admin.add_view(ModelView(ObservacionProfesor, "Observaciones Profesor",category="Observaciones"))
    admin.add_view(ModelView(Evento, "Eventos",category="Eventos"))
    admin.add_view(ModelView(Asistencia, "Asistencias", category="Asistencia y justificaciones"))
    admin.add_view(ModelView(Justificacion, "Justificaciones", category="Asistencia y justificaciones"))
    admin.add_view(ModelView(Archivo,"Archivos"))
    admin.add_view(ModelView(Video,"Videos"))
    admin.add_view(ViewWithMethodViews("Importador"))

add_views(admin)

if __name__ == '__main__':
    app.run(host=app.config.get('HOST', '127.0.0.1'),
            port=app.config.get('PORT', 4000))