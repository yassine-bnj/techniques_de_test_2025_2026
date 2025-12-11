"""Unit tests for the core triangulation and binary parsing logic."""

import pytest

from triangulator.core import decode_pointset, triangulate


def test_decode_empty_pointset():
    """Test decoding an empty PointSet (0 points)."""
    data = b"\x00\x00\x00\x00"
    points = decode_pointset(data)
    assert points == []


def test_decode_single_point():
    """Test decoding a PointSet with one point: (1.0, 2.0)."""
    data = b"\x01\x00\x00\x00" + b"\x00\x00\x80\x3f" + b"\x00\x00\x00\x40"
    points = decode_pointset(data)
    assert points == [(1.0, 2.0)]


def test_triangulate_too_few_points():
    """Test triangulation with fewer than 3 points (should return empty list)."""
    assert triangulate([]) == []
    assert triangulate([(0.0, 0.0)]) == []
    assert triangulate([(0.0, 0.0), (1.0, 1.0)]) == []


def test_triangulate_three_points():
    """Test triangulation of 3 non-collinear points."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = triangulate(points)
    assert len(triangles) == 1
    assert set(triangles[0]) == {0, 1, 2}


def test_triangulate_collinear_points():
    """Test triangulation of 3 collinear points (should return empty list)."""
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
    assert triangulate(points) == []


def test_decode_pointset_invalid_length():
    """Test decoding a PointSet with incorrect binary length."""
    with pytest.raises(ValueError):
        decode_pointset(b"\x05\x00\x00\x00")  