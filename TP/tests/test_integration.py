import pytest
import requests
from unittest.mock import patch
from triangulator.core import decode_pointset, triangulate, encode_triangles

# Simule un appel réel au PointSetManager (via mock)
@patch('requests.get')
def test_full_workflow(mock_get):
    # Simule une réponse binaire du PointSetManager
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"\x03\x00\x00\x00" + (b"\x00\x00\x80\x3f\x00\x00\x00\x40") * 3

    # Récupère les points
    resp = requests.get("http://fake-pointsetmanager/pointsets/123")
    points = decode_pointset(resp.content)  

    # Tente de trianguler
    triangles = triangulate(points) 

    # Encode le résultat
    result = encode_triangles(points, triangles)  

   
    assert result is not None