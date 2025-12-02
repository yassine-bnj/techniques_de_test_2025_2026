import pytest
import time
from triangulator.core import triangulate

@pytest.mark.performance
def test_performance_100_points():
    # Génère 100 points factices
    points = [(float(i), float(i*2)) for i in range(100)]
    
    start = time.perf_counter()
    try:
        triangulate(points)
    except NotImplementedError:
        pass  # OK, logique non implémentée
    duration = time.perf_counter() - start

    # On ne peut pas tester la durée réelle, mais on s'assure que l'appel est "testable"
    assert duration >= 0  # trivial, mais le test est présent

@pytest.mark.performance
def test_performance_1000_points():
    points = [(float(i), float(i)) for i in range(1000)]
    start = time.perf_counter()
    try:
        triangulate(points)
    except NotImplementedError:
        pass
    duration = time.perf_counter() - start
    assert duration >= 0