import os
import tempfile
import json
import pytest
from io import BytesIO
from os.path import dirname, abspath
import os
import api
from models.alumno import Alumno



@pytest.fixture
def client():
    db_fd, api.app.config['MONGO_DBNAME'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['MONGO_DBNAME'])

def test_get_alumno(client):
    alumno = Alumno.objects().first()
    if alumno == None:
        assert True
    else:
        rv = client.get('/alumno/'+str(alumno.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False