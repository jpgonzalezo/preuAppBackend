from flask_mongoengine import MongoEngine
from mongoengine import connect
db = MongoEngine()
connect('vr_kids')
