Module triangulator.core
========================
Core logic for Triangulator: binary parsing, triangulation, and encoding.

Functions
---------

`decode_pointset(data: bytes) ‑> list[tuple[float, float]]`
:   Decode a PointSet from binary data.
    
    The binary format is:
    - 4 bytes: number of points N (unsigned long, little-endian)
    - N × 8 bytes: (X: float, Y: float) for each point
    
    Raises:
        ValueError: if the data is too short or has an incorrect length.

`encode_triangles(vertices: list[tuple[float, float]], triangles: list[tuple[int, int, int]]) ‑> bytes`
:   Encode a list of triangles into the binary Triangles format.
    
    The binary format is:
    - PointSet (as in decode_pointset)
    - 4 bytes: number of triangles T (unsigned long)
    - T × 12 bytes: (i, j, k) vertex indices (unsigned long)
    
    Raises:
        ValueError: if any triangle index is out of bounds.

`triangulate(points: list[tuple[float, float]]) ‑> list[tuple[int, int, int]]`
:   Compute a triangulation from a list of 2D points.
    
    Returns a list of triangles as vertex index triples: [(i, j, k), ...].
    
    Minimal implementation:
    - Fewer than 3 points → empty list
    - 3 non-collinear points → single triangle [(0, 1, 2)]
    - More than 3 points → not supported (returns empty list)
    
    Args:
        points: List of (x, y) coordinates.
    
    Returns:
        List of triangles represented by vertex indices.