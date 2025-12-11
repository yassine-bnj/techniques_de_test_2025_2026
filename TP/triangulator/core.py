"""Core logic for Triangulator: binary parsing, triangulation, and encoding."""
import struct


def decode_pointset(data: bytes) -> list[tuple[float, float]]:
    """Decode a PointSet from binary data.

    The binary format is:
    - 4 bytes: number of points N (unsigned long, little-endian)
    - N × 8 bytes: (X: float, Y: float) for each point

    Raises:
        ValueError: if the data is too short or has an incorrect length.

    """
    if len(data) < 4:
        raise ValueError("Data too short to contain a PointSet")
    
    n_points = struct.unpack('<I', data[:4])[0]
    expected_length = 4 + n_points * 8
    if len(data) != expected_length:
        msg = f"Incorrect length: expected {expected_length}, got {len(data)}"
        raise ValueError(msg)

    points = []
    offset = 4
    for _ in range(n_points):
        x = struct.unpack('<f', data[offset:offset + 4])[0]
        y = struct.unpack('<f', data[offset + 4:offset + 8])[0]
        points.append((x, y))
        offset += 8

    return points


def encode_triangles(
    vertices: list[tuple[float, float]], triangles: list[tuple[int, int, int]]
) -> bytes:
    """Encode a list of triangles into the binary Triangles format.

    The binary format is:
    - PointSet (as in decode_pointset)
    - 4 bytes: number of triangles T (unsigned long)
    - T × 12 bytes: (i, j, k) vertex indices (unsigned long)

    Raises:
        ValueError: if any triangle index is out of bounds.

    """
    n_vertices = len(vertices)
    n_triangles = len(triangles)

    # Validate all vertex indices
    for tri in triangles:
        for idx in tri:
            if not (0 <= idx < n_vertices):
                raise ValueError(f"Invalid vertex index: {idx}")

    # Encode PointSet
    data = struct.pack('<I', n_vertices)
    for x, y in vertices:
        data += struct.pack('<ff', x, y)

    # Encode triangle indices
    data += struct.pack('<I', n_triangles)
    for i, j, k in triangles:
        data += struct.pack('<III', i, j, k)

    return data


def triangulate(points: list[tuple[float, float]]) -> list[tuple[int, int, int]]:
    """Compute a triangulation from a list of 2D points.

    Returns a list of triangles as vertex index triples: [(i, j, k), ...].

    Minimal implementation:
    - Fewer than 3 points → empty list
    - 3 non-collinear points → single triangle [(0, 1, 2)]
    - More than 3 points → not supported (returns empty list)

    Args:
        points: List of (x, y) coordinates.

    Returns:
        List of triangles represented by vertex indices.

    """
    if len(points) < 3:
        return []

    if len(points) == 3:
        # Compute signed area to check collinearity
        (x1, y1), (x2, y2), (x3, y3) = points
        area = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
        if abs(area) < 1e-6:
            return []  # collinear points
        return [(0, 1, 2)]

    # Triangulation for >3 points is not implemented in this minimal version
    return []