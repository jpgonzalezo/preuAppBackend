import os
import tempfile
import json
import pytest
from io import BytesIO
from os.path import dirname, abspath
import os
import api
from models.prueba import Prueba



@pytest.fixture
def client():
    db_fd, api.app.config['MONGO_DBNAME'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['MONGO_DBNAME'])

def test_get_prueba(client):
    prueba = Prueba.objects().first()
    if prueba == None:
        assert True
    else:
        rv = client.get('/pruebas/'+str(prueba.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_pruebas(client):
    rv = client.get('/pruebas')
    if rv._status_code == 200:
        assert True
    else:
        assert False