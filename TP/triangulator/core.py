def decode_pointset(data: bytes):
    """Décoder un PointSet à partir de données binaires."""
    raise NotImplementedError

def encode_triangles(vertices, triangles) -> bytes:
    """Encoder une liste de triangles au format binaire."""
    raise NotImplementedError

def triangulate(points):
    """
    Calculer une triangulation à partir d'une liste de points [(x, y), ...].
    Retourne une liste de triangles sous forme d'indices : [(i, j, k), ...].
    """
    raise NotImplementedError