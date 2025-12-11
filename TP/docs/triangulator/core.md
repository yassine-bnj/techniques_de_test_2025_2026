Module triangulator.core
========================

Functions
---------

`decode_pointset(data: bytes) ‑> List[Tuple[float, float]]`
:   Décoder un PointSet à partir de données binaires.
    
    Format:
    - 4 octets: nombre de points N (unsigned long, little-endian)
    - N fois 8 octets: (X: float, Y: float)
    
    Lève une ValueError si les données sont invalides.

`encode_triangles(vertices: List[Tuple[float, float]], triangles: List[Tuple[int, int, int]]) ‑> bytes`
:   Encoder une liste de triangles au format binaire Triangles.
    
    Format:
    - PointSet (comme decode_pointset)
    - 4 octets: nombre de triangles T
    - T fois 12 octets: (i, j, k) comme unsigned long
    
    Lève une ValueError si les indices sont invalides.

`triangulate(points: List[Tuple[float, float]]) ‑> List[Tuple[int, int, int]]`
:   Calculer une triangulation à partir d'une liste de points [(x, y), ...].
    Retourne une liste de triangles sous forme d'indices : [(i, j, k), ...].
    
    Implémentation minimale :
    - 0, 1, 2 points → []
    - 3 points non colinéaires → [(0, 1, 2)]
    - Plus de 3 points → non supporté (à étendre plus tard)