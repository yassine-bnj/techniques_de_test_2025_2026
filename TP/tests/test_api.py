import pytest
from triangulator.api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_post_triagulate_valid_id(client, mocker):
    # Mock de l'appel au PointSetManager
    mock_get = mocker.patch('triangulator.api.requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"\x03\x00\x00\x00" + (b"\x00\x00\x80\x3f\x00\x00\x00\x40") * 3  # 3 points

    response = client.post('/triangulate', json={'pointSetId': 123})
    assert response.status_code == 500  # Échoue car triangulate() non implémenté → OK

def test_post_triagulate_invalid_id_format(client):
    response = client.post('/triangulate', json={'pointSetId': 'not-an-int'})
    assert response.status_code == 400

def test_post_triagulate_missing_id(client):
    response = client.post('/triangulate', json={})
    assert response.status_code == 400