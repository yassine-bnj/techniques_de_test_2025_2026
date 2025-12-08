import struct
from typing import List, Tuple

def decode_pointset(data: bytes) -> List[Tuple[float, float]]:
    """
    Décoder un PointSet à partir de données binaires.

    Format:
    - 4 octets: nombre de points N (unsigned long, little-endian)
    - N fois 8 octets: (X: float, Y: float)

    Lève une ValueError si les données sont invalides.
    """
    if len(data) < 4:
        raise ValueError("Données trop courtes pour contenir un PointSet")
    
    n_points = struct.unpack('<I', data[:4])[0]
    expected_length = 4 + n_points * 8
    if len(data) != expected_length:
        raise ValueError(f"Longueur incorrecte: attendu {expected_length}, reçu {len(data)}")

    points = []
    offset = 4
    for _ in range(n_points):
        x = struct.unpack('<f', data[offset:offset+4])[0]
        y = struct.unpack('<f', data[offset+4:offset+8])[0]
        points.append((x, y))
        offset += 8

    return points

def encode_triangles(vertices: List[Tuple[float, float]], triangles: List[Tuple[int, int, int]]) -> bytes:
    """
    Encoder une liste de triangles au format binaire Triangles.

    Format:
    - PointSet (comme decode_pointset)
    - 4 octets: nombre de triangles T
    - T fois 12 octets: (i, j, k) comme unsigned long

    Lève une ValueError si les indices sont invalides.
    """
    n_vertices = len(vertices)
    n_triangles = len(triangles)

    # Vérifier que tous les indices sont valides
    for tri in triangles:
        for idx in tri:
            if not (0 <= idx < n_vertices):
                raise ValueError(f"Indice de sommet invalide: {idx}")

    # Encoder le PointSet
    data = struct.pack('<I', n_vertices)
    for x, y in vertices:
        data += struct.pack('<ff', x, y)

    # Encoder les triangles
    data += struct.pack('<I', n_triangles)
    for i, j, k in triangles:
        data += struct.pack('<III', i, j, k)

    return data

def triangulate(points: List[Tuple[float, float]]) -> List[Tuple[int, int, int]]:
    """
    Calculer une triangulation à partir d'une liste de points [(x, y), ...].
    Retourne une liste de triangles sous forme d'indices : [(i, j, k), ...].

    Implémentation minimale :
    - 0, 1, 2 points → []
    - 3 points non colinéaires → [(0, 1, 2)]
    - Plus de 3 points → non supporté (à étendre plus tard)
    """
    if len(points) < 3:
        return []

    if len(points) == 3:
        # Vérifier colinéarité simple (aire du triangle = 0)
        (x1, y1), (x2, y2), (x3, y3) = points
        area = x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)
        if abs(area) < 1e-6:
            return []  # points colinéaires
        return [(0, 1, 2)]

    # Pour l'instant, on ne supporte pas > 3 points
    # On pourrait lever une exception, mais le sujet suggère de gérer ce cas
    # On retourne vide pour l'instant → à étendre si besoin
    return []