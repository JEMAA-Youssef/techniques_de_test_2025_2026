"""Fonctions utilitaires d'encodage et de décodage binaire pour les PointSet.

Un PointSet est représenté comme une liste de tuples ``[(x, y), ...]`` et sa
forme binaire suit les conventions définies dans le sujet :

- 4 octets : nombre de points (unsigned long, big-endian)
- pour chaque point : 4 octets float (x), puis 4 octets float (y)
"""

import struct


def encode_pointset(points):
    """Encode a set of points into the binary ``PointSet`` format.

    Format binaire :
    - 4 octets : nombre de points (unsigned long)
    - puis pour chaque point : 4 octets float (x), 4 octets float (y).
    """
    if not isinstance(points, list):
        raise ValueError("Points must be a list of (x, y) tuples")

    count = len(points)
    buffer = struct.pack(">I", count)

    for x, y in points:
        buffer += struct.pack(">ff", float(x), float(y))

    return buffer


def decode_pointset(binary_data):
    """Décoder un PointSet binaire vers une liste de tuples (x, y).

    Le format attendu doit avoir :
    - 4 octets indiquant le nombre de points ;
    - puis 8 octets par point.

    Lève ValueError si la taille est incohérente ou trop courte.
    """
    if len(binary_data) < 4:
        raise ValueError("Binary data too short")

    count = struct.unpack(">I", binary_data[:4])[0]
    expected_len = 4 + count * 8

    if len(binary_data) != expected_len:
        raise ValueError("Invalid binary length for PointSet")

    points = []
    offset = 4

    for _ in range(count):
        x, y = struct.unpack(">ff", binary_data[offset:offset + 8])
        points.append((x, y))
        offset += 8

    return points
