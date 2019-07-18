import os
import tempfile
import json
import pytest
from io import BytesIO
from os.path import dirname, abspath
import os
import api
from models.curso import Curso



@pytest.fixture
def client():
    db_fd, api.app.config['MONGO_DBNAME'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['MONGO_DBNAME'])

def test_get_curso(client):
    curso = Curso.objects().first()
    if curso == None:
        assert True
    else:
        rv = client.get('/cursos/'+str(curso.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_cursos(client):
    rv = client.get('/cursos')
    if rv._status_code == 200:
        assert True
    else:
        assert False