from db import db
from flask import send_file
from datetime import datetime
from models.asignatura import Asignatura
from models.curso import Curso
import mongoengine_goodjson as gj
import os
from werkzeug.utils import secure_filename


class Video(gj.Document):
    nombre = db.StringField(verbose_name="Nombre Video", max_length=200)
    uri = db.StringField(verbose_name="Uri", max_length=200)
    asignatura = db.ReferenceField(Asignatura)
    curso = db.ReferenceField(Curso)
    fecha = db.DateTimeField(default=datetime.now)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "uri": self.uri,
            "asignatura": self.asignatura.to_dict(),
            "curso": self.curso.to_dict(),
            "fecha": self.fecha.strftime("%m/%d/%Y, %H:%M:%S")
        }

    # literal los class method son los services en java
    @classmethod
    def create(cls, new_video):
        asignatura = Asignatura.objects(id=new_video["asignatura_id"]).first()
        curso = Curso.objects(id=new_video["curso_id"]).first()
        id_video = new_video['uri'].split("?v=")
        id_video =id_video[1]
        if "&" in id_video:
            id_video = id_video.split("&")[0]
        embed_link = "http://www.youtube.com/embed/" + id_video
        video = Video(nombre=new_video['nombre'], uri=embed_link,
                      asignatura=asignatura, curso=curso)
        video.save()
        return video.to_dict()

    @classmethod
    def get_all(cls):
        videos = Video.objects().all()
        result_list = []
        for video in videos:
            result_list.append(video.to_dict())
        return result_list

    @classmethod
    def get_all_by_asignatura(cls, asignatura_id):
        videos = Video.objects(asignatura=asignatura_id).all()
        result_list = []
        for video in videos:
            result_list.append(video.to_dict())
        return result_list

    @classmethod
    def get_all_by_asignatura_and_curso(cls, asignatura_id, curso_id):
        videos = Video.objects(asignatura=asignatura_id, curso=curso_id).all()
        result_list = []
        for video in videos:
            result_list.append(video.to_dict())
        return result_list

    @classmethod
    def get_by_id(cls, video_id):
        video = Video.objects(id=video_id).first()
        return video.to_dict()


    @classmethod
    def erase(cls, video_id):
        video = Video.objects(id=video_id).first()
        video.delete()
        return "Video eliminado"
         