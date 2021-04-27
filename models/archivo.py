from db import db
from flask import send_file
from datetime import datetime
from models.asignatura import Asignatura
import mongoengine_goodjson as gj
import os
from werkzeug.utils import secure_filename


class Archivo(gj.Document):
    nombre = db.StringField(verbose_name="Nombre Archivo", max_length=200)
    path = db.StringField(verbose_name="Path", max_length=200)
    asignatura = db.ReferenceField(Asignatura)
    fecha = db.DateTimeField(default=datetime.now)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "path": self.path,
            "asignatura": self.asignatura.to_dict(),
            "fecha": self.fecha.strftime("%m/%d/%Y %H:%M:%S")
        }

    # literal los class method son los services en java
    @classmethod
    def upload(cls, base_path, new_file, asignatura_id):
        asignatura = Asignatura.objects(id=asignatura_id).first()
        folder = base_path + asignatura_id
        if not os.path.exists(folder):
            os.mkdir(folder)
        file_name = secure_filename(new_file.filename)
        path = os.path.join(folder, file_name)
        new_file.save(path)
        if os.path.exists(path):
            archivo = Archivo(nombre=file_name, path=path,
                              asignatura=asignatura)
            archivo.save()
        return archivo.to_dict()
    
    @classmethod
    def get_all_by_asignatura(cls, asignatura_id):
        archivos = Archivo.objects(asignatura = asignatura_id).all()
        result_list=[]
        for archivo in archivos:
            result_list.append(archivo.to_dict())
        return result_list

    @classmethod
    def download(cls, archivo_id):
        archivo = Archivo.objects(id=archivo_id).first()
        print(60*"*", archivo.path)
        return send_file(archivo.path, as_attachment=True, attachment_filename=archivo.nombre + "")

    @classmethod
    def erase(cls, archivo_id):
        try:
            archivo = Archivo.objects(id=archivo_id).first()
            os.remove(archivo.path)
            archivo.delete()
            return "Archivo eliminado"
        except Exception as e:
            print(str(e))
            return "No se pudo eliminar el archivo"
    
    @classmethod
    def get_all(cls):
        archivos = Archivo.objects().all()
        result_list = []
        for archivo in archivos:
            result_list.append(archivo.to_dict())
        return result_list