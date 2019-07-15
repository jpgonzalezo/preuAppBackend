import os
import tempfile
import json
import pytest
from io import BytesIO
from os.path import dirname, abspath
import os
import api
from models.profesor import Profesor



@pytest.fixture
def client():
    db_fd, api.app.config['MONGO_DBNAME'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['MONGO_DBNAME'])

def test_get_profesor(client):
    profesor = Profesor.objects().first()
    if profesor == None:
        assert True
    else:
        rv = client.get('/profesores/'+str(profesor.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_profesores(client):
    rv = client.get('/profesores')
    if rv._status_code == 200:
        assert True
    else:
        assert False