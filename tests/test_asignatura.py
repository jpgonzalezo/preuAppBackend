import os
import tempfile
import json
import pytest
from io import BytesIO
from os.path import dirname, abspath
import os
import api
from models.asignatura import Asignatura



@pytest.fixture
def client():
    db_fd, api.app.config['MONGO_DBNAME'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['MONGO_DBNAME'])

def test_get_alerta(client):
    asignatura = Asignatura.objects().first()
    if asignatura == None:
        assert True
    else:
        rv = client.get('/asignaturas/'+str(asignatura.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_alertas(client):
    rv = client.get('/asignaturas')
    if rv._status_code == 200:
        assert True
    else:
        assert False