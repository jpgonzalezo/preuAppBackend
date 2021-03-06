import os
import tempfile
import json
import pytest
from io import BytesIO
from os.path import dirname, abspath
import os
import api
from models.justificacion import Justificacion



@pytest.fixture
def client():
    db_fd, api.app.config['MONGO_DBNAME'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['MONGO_DBNAME'])

def test_get_justificacion(client):
    justificacion = Justificacion.objects().first()
    if justificacion == None:
        assert True
    else:
        rv = client.get('/justificaciones/'+str(justificacion.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_justificaciones(client):
    rv = client.get('/justificaciones')
    if rv._status_code == 200:
        assert True
    else:
        assert False