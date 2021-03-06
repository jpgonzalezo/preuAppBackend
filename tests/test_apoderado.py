import os
import tempfile
import json
import pytest
from io import BytesIO
from os.path import dirname, abspath
import os
import api
from models.apoderado import Apoderado



@pytest.fixture
def client():
    db_fd, api.app.config['MONGO_DBNAME'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['MONGO_DBNAME'])

def test_get_apoderado(client):
    apoderado = Apoderado.objects().first()
    if apoderado == None:
        assert True
    else:
        rv = client.get('/apoderados/'+str(apoderado.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_apoderados(client):
    rv = client.get('/apoderados')
    if rv._status_code == 200:
        assert True
    else:
        assert False