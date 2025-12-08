import pytest
from triangulator.api import app
import struct
@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_post_triagulate_valid_id(client, mocker):
    # 3 points non colinéaires
    mock_content = (
        b"\x03\x00\x00\x00" +
        struct.pack('<ff', 0.0, 0.0) +
        struct.pack('<ff', 1.0, 0.0) +
        struct.pack('<ff', 0.0, 1.0)
    )
    mock_get = mocker.patch('triangulator.api.requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = mock_content

    response = client.post('/triangulate', json={'pointSetId': 123})

    assert response.status_code == 200
    assert response.content_type == 'application/octet-stream'

    data = response.data
    # Taille attendue : 4 + 3*8 + 4 + 1*12 = 4 + 24 + 4 + 12 = 44
    assert len(data) == 44

    # Optionnel : vérifier les indices
    n_triangles = struct.unpack('<I', data[28:32])[0]
    assert n_triangles == 1

    i, j, k = struct.unpack('<III', data[32:44])
    assert {i, j, k} == {0, 1, 2}

def test_post_triagulate_invalid_id_format(client):
    response = client.post('/triangulate', json={'pointSetId': 'not-an-int'})
    assert response.status_code == 400

def test_post_triagulate_missing_id(client):
    response = client.post('/triangulate', json={})
    assert response.status_code == 400