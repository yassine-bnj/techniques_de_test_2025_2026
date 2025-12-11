"""Test the Triangulator API endpoints."""

import struct

import pytest
import requests

from triangulator.api import app


@pytest.fixture
def client():
    """Flask test client configured for testing."""
    app.config["TESTING"] = True
    return app.test_client()


def test_post_triagulate_valid_id(client, mocker):
    """Test successful triangulation request with valid PointSetID."""
    mock_content = (
        b"\x03\x00\x00\x00"
        + struct.pack("<ff", 0.0, 0.0)
        + struct.pack("<ff", 1.0, 0.0)
        + struct.pack("<ff", 0.0, 1.0)
    )
    mock_get = mocker.patch("triangulator.api.requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = mock_content

    response = client.post("/triangulate", json={"pointSetId": 123})

    assert response.status_code == 200
    assert response.content_type == "application/octet-stream"

    data = response.data
    assert len(data) == 44  # 4 + 3*8 + 4 + 12

    n_triangles = struct.unpack("<I", data[28:32])[0]
    assert n_triangles == 1

    i, j, k = struct.unpack("<III", data[32:44])
    assert {i, j, k} == {0, 1, 2}


def test_post_triagulate_invalid_id_format(client):
    """Test request with non-integer pointSetId."""
    response = client.post("/triangulate", json={"pointSetId": "not-an-int"})
    assert response.status_code == 400


def test_post_triagulate_missing_id(client):
    """Test request missing 'pointSetId' field."""
    response = client.post("/triangulate", json={})
    assert response.status_code == 400


def test_post_triagulate_non_json_content(client):
    """Test request with non-JSON content type."""
    response = client.post(
        "/triangulate", data="not json", content_type="text/plain"
    )
    assert response.status_code == 400


def test_post_triagulate_negative_id(client):
    """Test request with negative pointSetId."""
    response = client.post("/triangulate", json={"pointSetId": -5})
    assert response.status_code == 400


def test_post_triagulate_pointsetmanager_unreachable(client, mocker):
    """Test request when PointSetManager is unreachable."""
    mocker.patch(
        "triangulator.api.requests.get",
        side_effect=requests.RequestException()
    )
    response = client.post("/triangulate", json={"pointSetId": 123})
    assert response.status_code == 502