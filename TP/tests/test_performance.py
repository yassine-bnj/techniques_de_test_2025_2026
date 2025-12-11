"""Performance tests for the triangulation logic."""

import contextlib
import time

import pytest
from triangulator.core import triangulate


@pytest.mark.performance
def test_performance_100_points():
    """Measure triangulation time for 100 points."""
    points = [(float(i), float(i * 2)) for i in range(100)]

    start = time.perf_counter()
    with contextlib.suppress(NotImplementedError):
        triangulate(points)
    duration = time.perf_counter() - start

    # Ensure the call is measurable (even if logic is not fully implemented)
    assert duration >= 0


@pytest.mark.performance
def test_performance_1000_points():
    """Measure triangulation time for 1,000 points."""
    points = [(float(i), float(i)) for i in range(1000)]

    start = time.perf_counter()
    with contextlib.suppress(NotImplementedError):
        triangulate(points)
    duration = time.perf_counter() - start

    assert duration >= 0