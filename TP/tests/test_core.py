import pytest
from triangulator.core import decode_pointset, triangulate, encode_triangles

def test_decode_empty_pointset():
    # 0 point → 4 octets = 0
    data = b"\x00\x00\x00\x00"
    points = decode_pointset(data)
    assert points == []

def test_decode_single_point():
    # 1 point : (1.0, 2.0)
    # nb_points = 1 → b"\x01\x00\x00\x00"
    # x = 1.0 → b"\x00\x00\x80\x3f"
    # y = 2.0 → b"\x00\x00\x00\x40"
    data = b"\x01\x00\x00\x00" + b"\x00\x00\x80\x3f" + b"\x00\x00\x00\x40"
    points = decode_pointset(data)
    assert points == [(1.0, 2.0)]

def test_triangulate_too_few_points():
    assert triangulate([]) == []
    assert triangulate([(0.0, 0.0)]) == []
    assert triangulate([(0.0, 0.0), (1.0, 1.0)]) == []

def test_triangulate_three_points():
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = triangulate(points)
    # On attend 1 triangle avec indices (0, 1, 2) — ordre peut varier
    assert len(triangles) == 1
    assert set(triangles[0]) == {0, 1, 2}

def test_triangulate_collinear_points():
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]  # colinéaires
    assert triangulate(points) == []

def test_decode_pointset_invalid_length():
    with pytest.raises(ValueError):
        decode_pointset(b"\x05\x00\x00\x00")  # 5 points attendus, mais 0 fourni    