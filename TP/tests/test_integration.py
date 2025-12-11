"""Integration tests for the Triangulator microservice."""

from unittest.mock import patch

import requests
from triangulator.core import decode_pointset, encode_triangles, triangulate


@patch("requests.get")
def test_full_workflow(mock_get):
    """Test the full workflow: fetch PointSet, triangulate, and encode result.

    Simulates a successful interaction with the PointSetManager and verifies
    that the core functions can process the binary data and produce a result.
    """
    # Build mock binary response: 3 identical points (1.0, 2.0)
    point_bytes = b"\x00\x00\x80\x3f\x00\x00\x00\x40"  # (1.0, 2.0)
    mock_content = b"\x03\x00\x00\x00" + point_bytes * 3
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = mock_content

    # Simulate fetching from PointSetManager
    resp = requests.get("http://fake-pointsetmanager/pointsets/123")
    points = decode_pointset(resp.content)

    # Perform triangulation
    triangles = triangulate(points)

    # Encode result
    result = encode_triangles(points, triangles)

    # Ensure a binary result is produced
    assert result is not None