from flask import Flask, Blueprint, jsonify, request, send_file, current_app
from models.alumno import Alumno
from models.direccion import Direccion
from models.colegio import Colegio
from models.apoderado import Apoderado
from models.administrador import Administrador
from models.profesor import Profesor
from models.curso import Curso
from utils.excel_util import sheet_Tupla as excel_read
from models.evaluacion import Evaluacion
from models.prueba import Prueba
from models.asignatura import Asignatura
from models.asistencia import Asistencia
from models.observacion import Observacion
from models.prueba import Prueba
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from bson import json_util
from PIL import Image
from flask_restful import reqparse
import os


def init_module(api):
    api.add_resource(AlumnoItem, '/alumno/<id>')
    api.add_resource(AlumnoToken, '/alumno/token')
    api.add_resource(Alumnos, '/alumnos')
    api.add_resource(AlumnoHojaVida, '/hoja_vida/<id>')
    api.add_resource(AlumnoImagenItem, '/alumno_imagen/<id>')
    api.add_resource(AlumnoImagenDefault, '/alumno_imagen_default/<id>')
    api.add_resource(AlumnosCurso, '/alumnos_curso/<id_curso>')
    api.add_resource(AlumnoGraficoRendimiento,
                     '/alumno_grafico_rendimiento/<id>')
    api.add_resource(AlumnoGraficoAsistencia,
                     '/alumno_grafico_asistencia/<id>')
    api.add_resource(AlumnoExcel, '/alumnoExcel')


class AlumnoGraficoAsistencia(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'auth-token', type=str, required=True, location='headers')
        super(AlumnoGraficoAsistencia, self).__init__()

    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'}, 401
        labels = []
        data_asistencia_asignatura = []
        data_inasistencia_asignatura = []
        data_asistencia_anual = []
        data_inasistencia_anual = []
        labels_anual = ['Mar', 'Abr', 'May', 'Jun',
                        'Jul', 'Ago', 'Sep', 'Oct', 'Nov']
        meses = [3, 4, 5, 6, 7, 8, 9, 10, 11]
        alumno = Alumno.objects(id=id).first()
        for asignatura in alumno.curso.asignaturas:
            labels.append(asignatura.nombre)
            presentes = 0
            for asistencia in Asistencia.objects(asignatura=asignatura,curso=alumno.curso).all():
                if alumno in asistencia.alumnos_presentes:
                    presentes = presentes + 1
            if Asistencia.objects(asignatura=asignatura,curso=alumno.curso).count() > 0:
                presentes = int(
                    (presentes/Asistencia.objects(asignatura=asignatura,curso=alumno.curso).count())*100)
            data_asistencia_asignatura.append(presentes)
            data_inasistencia_asignatura.append(100-presentes)

        for mes in meses:
            asistencia_mes = 0
            cant_asistencia = 0
            aprobacion = 0
            for asistencia in Asistencia.objects(curso=alumno.curso).all():
                if str(asistencia.fecha.month) == str(mes):
                    cant_asistencia = cant_asistencia + 1
                    if alumno in asistencia.alumnos_presentes:
                        asistencia_mes = asistencia_mes + 1
            if cant_asistencia > 0:
                aprobacion = int((asistencia_mes/cant_asistencia)*100)
            data_asistencia_anual.append(aprobacion)
            data_inasistencia_anual.append(100-aprobacion)

        return {
            "grafico_asignatura": {
                "labels": labels,
                "data": [
                    {"data": data_asistencia_asignatura, "label": "Asistencia (%)"}
                ]
            },
            "grafico_anual": {
                "labels": labels_anual,
                "data": [
                    {"data": data_asistencia_anual, "label": "Asistencia (%)"}
                ]
            }
        }


class AlumnoGraficoRendimiento(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'auth-token', type=str, required=True, location='headers')
        super(AlumnoGraficoRendimiento, self).__init__()

    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'}, 401
        labels = []
        data_ensayo = []
        data_taller = []
        data_tarea = []
        alumno = Alumno.objects(id=id).first()
        for asignatura in alumno.curso.asignaturas:
            labels.append(asignatura.nombre)
            suma_ensayo = 0
            suma_taller = 0
            suma_tarea = 0
            for prueba in Prueba.objects(asignatura=asignatura, tipo="ENSAYO").all():
                puntaje = 0
                evaluacion = Evaluacion.objects(
                    alumno=alumno.id, prueba=prueba.id).first()
                if evaluacion != None:
                    puntaje = evaluacion.puntaje
                suma_ensayo = suma_ensayo + puntaje

            for prueba in Prueba.objects(asignatura=asignatura, tipo="TALLER").all():
                puntaje = 0
                evaluacion = Evaluacion.objects(
                    alumno=alumno.id, prueba=prueba.id).first()
                if evaluacion != None:
                    puntaje = evaluacion.puntaje
                suma_taller = suma_taller + puntaje

            for prueba in Prueba.objects(asignatura=asignatura, tipo="TAREA").all():
                puntaje = 0
                evaluacion = Evaluacion.objects(
                    alumno=alumno.id, prueba=prueba.id).first()
                if evaluacion != None:
                    puntaje = evaluacion.puntaje
                suma_tarea = suma_tarea + puntaje

            if Prueba.objects(asignatura=asignatura, tipo="ENSAYO").count() > 0:
                data_ensayo.append(
                    int((suma_ensayo/Prueba.objects(asignatura=asignatura, tipo="ENSAYO").count())))
            if Prueba.objects(asignatura=asignatura, tipo="ENSAYO").count() == 0:
                data_ensayo.append(int(suma_ensayo))

            if Prueba.objects(asignatura=asignatura, tipo="TALLER").count() > 0:
                data_taller.append(
                    int((suma_taller/Prueba.objects(asignatura=asignatura, tipo="TALLER").count())))
            if Prueba.objects(asignatura=asignatura, tipo="TALLER").count() == 0:
                data_taller.append(int(suma_taller))

            if Prueba.objects(asignatura=asignatura, tipo="TAREA").count() > 0:
                data_tarea.append(
                    int((suma_tarea/Prueba.objects(asignatura=asignatura, tipo="TAREA").count())))
            if Prueba.objects(asignatura=asignatura, tipo="TAREA").count() == 0:
                data_tarea.append(int(suma_tarea))

        return{
            "labels": labels,
            "data": [
                {"data": data_ensayo, "label": "Ensayo"},
                {"data": data_taller, "label": "Taller"},
                {"data": data_tarea, "label": "Tarea"}
            ]
        }


class AlumnosCurso(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'auth-token', type=str, required=True, location='headers')
        super(AlumnosCurso, self).__init__()

    def get(self, id_curso):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'}, 401
        alumnos = []
        curso = Curso.objects(id=id_curso).first()
        for alumno in Alumno.objects(curso=curso.id, activo=True).all():
            if alumno.activo:
                alumnos.append(alumno.to_dict())
        return alumnos


class AlumnoHojaVida(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'auth-token', type=str, required=True, location='headers')
        super(AlumnoHojaVida, self).__init__()

    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'}, 401
        alumno = Alumno.objects(id=id).first()
        evaluaciones = Evaluacion.objects(alumno=alumno.id).all()
        evaluaciones_matematicas = []
        evaluaciones_lenguaje = []
        ponderacion_matematicas = 0
        ponderacion_lenguaje = 0
        colegio = ""
        if alumno.colegio != None:
            colegio = alumno.colegio.nombre
        for evaluacion in evaluaciones:
            if (evaluacion.prueba.asignatura.nombre == 'Matemáticas') and (evaluacion.prueba.tipo != "TAREA"):
                evaluaciones_matematicas.append(evaluacion)

            if (evaluacion.prueba.asignatura.nombre == 'Lenguaje') and (evaluacion.prueba.tipo != "TAREA"):
                evaluaciones_lenguaje.append(evaluacion)

        for evaluacion_mat in evaluaciones_matematicas:
            ponderacion_matematicas = ponderacion_matematicas + evaluacion_mat.puntaje

        for evaluacion_leng in evaluaciones_lenguaje:
            ponderacion_lenguaje = ponderacion_lenguaje + evaluacion_leng.puntaje

        promedio_mat = 0
        promedio_leng = 0

        if ponderacion_matematicas > 0:
            promedio_mat = int((ponderacion_matematicas) /
                               evaluaciones_matematicas.__len__())

        if ponderacion_lenguaje > 0:
            promedio_leng = int((ponderacion_lenguaje) /
                                evaluaciones_lenguaje.__len__())

        asistencias = Asistencia.objects(curso=alumno.curso).all()
        cantidad_presente = 0
        for asistencia in asistencias:
            for alumno_presente in asistencia.alumnos_presentes:
                if alumno_presente.id == alumno.id:
                    cantidad_presente = cantidad_presente + 1

        promedio_asistencia = 0
        if cantidad_presente > 0:
            promedio_asistencia = int(
                100*(cantidad_presente/asistencias.__len__()))

        observaciones = json.loads(
            Observacion.objects(alumno=alumno).all().to_json())

        return {
            'id': str(alumno.id),
            'nombres': alumno.nombres,
            'calegio': colegio,
            'curso': alumno.curso.nombre,
            'curso_id': str(alumno.curso.id),
            'apellido_paterno': alumno.apellido_paterno,
            'apellido_materno': alumno.apellido_materno,
            'telefono': alumno.telefono,
            'email': alumno.email,
            'ponderacion_matematicas': promedio_mat,
            'ponderacion_lenguaje': promedio_leng,
            'ponderacion_asistencia': promedio_asistencia,
            'observaciones': observaciones,
            'imagen': alumno.imagen,
            'direccion': alumno.direccion.calle+" "+alumno.direccion.numero+", "+alumno.direccion.comuna
        }


class AlumnoToken(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'auth-token', type=str, required=True, location='headers')
        super(AlumnoToken, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        if alumno == None and apoderado == None:
            return {'response': 'user_invalid'}, 401
        if alumno != None:
            return alumno.to_dict()
        if apoderado != None:
            return apoderado.alumno.to_dict()


class AlumnoItem(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'auth-token', type=str, required=True, location='headers')
        super(AlumnoItem, self).__init__()

    def put(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.objects(id=id).first()
        administrador = Administrador.load_from_token(token)
        if alumno == None and administrador == None:
            return {'response': 'user_invalid'}, 401
        data = request.data.decode()
        data = json.loads(data)
        alumno.nombres = data['nombres']
        alumno.apellido_paterno = data['apellido_paterno']
        alumno.apellido_materno = data['apellido_materno']
        alumno.telefono = data['telefono']
        alumno.email = data['email']
        alumno.sexo = data['sexo']
        alumno.rut = data['rut']
        alumno.puntaje_ingreso = data['puntaje_ingreso']
        direccion = Direccion(calle=data['calle'],
                              numero=data['numero'],
                              comuna=data['comuna'],
                              cas_dep_of=data['cas_dep_of'])
        alumno.direccion = direccion
        colegio = Colegio.objects(id=data['colegio']).first()
        curso = Curso.objects(id=data['curso']).first()
        alumno.colegio = colegio
        alumno.curso = curso
        alumno.save()
        colegio.updateCantEstudiantes()
        curso.updateCantEstudiantes()
        colegio.save()
        curso.save()
        return {'Response': 'exito',
                'id': str(alumno.id)}

    def get(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'}, 401
        return Alumno.objects(id=id).first().to_dict()

    def delete(self, id):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'}, 401
        alumno = Alumno.objects(id=id).first()
        alumno.activo = False
        alumno.save()
        colegio = Colegio.objects(id=alumno.colegio.id).first()
        curso = Curso.objects(id=alumno.curso.id).first()
        colegio.updateCantEstudiantes()
        curso.updateCantEstudiantes()
        colegio.save()
        curso.save()
        return{'Response': 'borrado'}


class Alumnos(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'auth-token', type=str, required=True, location='headers')
        super(Alumnos, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'}, 401
        response = []
        for alumno in Alumno.objects(activo=True).all():
            response.append(alumno.to_dict())
        return response

    def post(self):
        args = self.reqparse.parse_args()
        token = args.get('auth-token')
        alumno = Alumno.load_from_token(token)
        apoderado = Apoderado.load_from_token(token)
        administrador = Administrador.load_from_token(token)
        profesor = Profesor.load_from_token(token)
        if alumno == None and apoderado == None and administrador == None and profesor == None:
            return {'response': 'user_invalid'}, 401
        data = request.data.decode()
        data = json.loads(data)
        alumno = Alumno()
        alumno.nombres = data['nombres']
        alumno.apellido_paterno = data['apellido_paterno']
        alumno.apellido_materno = data['apellido_materno']
        alumno.telefono = data['telefono']
        alumno.email = data['email']
        alumno.encrypt_password(data['rut'])
        alumno.sexo = data['sexo']
        alumno.rut = data['rut']
        alumno.puntaje_ingreso = data['puntaje_ingreso']
        direccion = Direccion(calle=data['calle'],
                              numero=data['numero'],
                              comuna=data['comuna'],
                              cas_dep_of=data['cas_dep_of'])
        alumno.direccion = direccion
        colegio = Colegio.objects(id=data['colegio']).first()
        curso = Curso.objects(id=data['curso']).first()
        alumno.colegio = colegio
        alumno.curso = curso
        alumno.save()
        colegio.updateCantEstudiantes()
        curso.updateCantEstudiantes()
        colegio.save()
        curso.save()
        return {'Response': 'exito',
                'id': str(alumno.id)}


class AlumnoImagenItem(Resource):
    def post(self, id):
        imagen = Image.open(request.files['imagen'].stream).convert("RGB")
        print(60*"*", os.path.join(current_app.config.get("BASE_PATH")+"uploads/alumnos", str(id)+".jpg"))
        imagen.save(os.path.join(current_app.config.get("BASE_PATH")+"uploads/alumnos", str(id)+".jpg"))
        imagen.thumbnail((800, 800))
        imagen.save(os.path.join(current_app.config.get("BASE_PATH")+"uploads/alumnos", str(id)+'_thumbnail.jpg'))
        alumno = Alumno.objects(id=id).first()
        alumno.imagen = id
        alumno.save()
        return {'Response': 'exito'}

    def get(self, id):
        return send_file(current_app.config.get("BASE_PATH")+'uploads/alumnos/'+id+'_thumbnail.jpg')


class AlumnoImagenDefault(Resource):
    def get(self, id):
        alumno = Alumno.objects(id=id).first()
        imagen = Image.open(current_app.config.get("BASE_PATH")+"uploads/alumnos/default_thumbnail.jpg")
        imagen.thumbnail((800, 800))
        imagen.save(os.path.join(current_app.config.get("BASE_PATH")+"uploads/alumnos", str(id)+'_thumbnail.jpg'))
        alumno.imagen = str(alumno.id)
        alumno.save()
        return {'Response': 'exito'}


class AlumnoExcel(Resource):
    def get(self):
        return Alumno.create_layout_excel()

    # TODO: añadir validaciones: si no viene el archivo
    def post(self):
        file = request.files["file"]
        lista = excel_read(file)
        response = Alumno.create_from_excel(lista)
        if(response == "hecho"):
            return {'Response': response}
        else:
            return response
