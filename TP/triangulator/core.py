"""Core triangulation logic for the Triangulator microservice.

This module provides:

* validation of ``PointSet`` identifiers (UUID) ;
* retrieval of binary point sets from the PointSetManager ;
* a simple fan triangulation algorithm ;
* encoding of the resulting triangles into the binary format.
"""

import struct
import uuid

import requests

from .binary_utils import encode_pointset


def _validate_uuid(pointset_id: str) -> uuid.UUID:
    """Validate that the given identifier is a proper UUID.

    Raise :class:`ValueError` if the identifier is invalid (mapped to
    HTTP 400 by the API layer).
    """
    try:
        return uuid.UUID(pointset_id)
    except Exception as exc:
        raise ValueError("Invalid PointSet ID format") from exc


def _fetch_pointset_from_manager(pointset_id: str) -> bytes:
    """Récupérer un PointSet binaire depuis le PointSetManager.

    Exceptions possibles :
    - FileNotFoundError → si le service renvoie 404
    - RuntimeError → si le service renvoie 503
    - Exception générique → pour tout autre code d'erreur
    """
    url = f"http://localhost:5000/pointsets/{pointset_id}"
    try:
        response = requests.get(url)
    except Exception as exc:
        raise RuntimeError("Service PointSetManager unavailable") from exc

    if response.status_code == 404:
        raise FileNotFoundError("PointSet not found")

    if response.status_code == 503:
        raise RuntimeError("PointSetManager unavailable")

    if response.status_code != 200:
        raise Exception("Unexpected PointSetManager error")

    return response.content


def _triangulate_points(points):
    """Compute a fan triangulation from a list of points.

    The input is a list of ``(x, y)`` tuples. The result is a list
    of triangles represented by index triplets ``(i, j, k)`` into the
    original list of points.
    """
    n = len(points)

    if n < 3:
        return []  # aucun triangle possible

    # Triangulation simple : (0, i, i+1)
    triangles = []
    for i in range(1, n - 1):
        triangles.append((0, i, i + 1))

    return triangles


def _encode_triangles(points, triangles):
    """Encode triangles to the binary format defined in the assignment.

    The representation concatenates the ``PointSet`` encoding, then:

    * 4 bytes ``unsigned long`` for the number of triangles ;
    * for each triangle, three indices stored as 4-byte unsigned longs.
    """
    pointset_binary = encode_pointset(points)
    tri_count = len(triangles)

    binary_triangles = struct.pack(">I", tri_count)

    for i, j, k in triangles:
        binary_triangles += struct.pack(">III", i, j, k)

    return pointset_binary + binary_triangles


def triangulate(pointset_id: str) -> bytes:
    """Perform the full triangulation workflow for a given identifier.

    The workflow is:

    1. validate the UUID ;
    2. fetch the binary ``PointSet`` ;
    3. decode it into a list of points ;
    4. run the triangulation algorithm ;
    5. encode the result into the binary ``Triangles`` format.

    Expected exceptions used by the API mapping are:

    * :class:`ValueError` → HTTP 400 ;
    * :class:`FileNotFoundError` → HTTP 404 ;
    * :class:`RuntimeError` → HTTP 503 ;
    * generic :class:`Exception` → HTTP 500.
    """
    from .binary_utils import decode_pointset  # éviter les boucles d'import

    # 1) Validation UUID (tests API → 400)
    _validate_uuid(pointset_id)

    # 2) Récupération du pointset
    binary_data = _fetch_pointset_from_manager(pointset_id)

    # 3) Décodage
    points = decode_pointset(binary_data)

    # 4) Triangulation interne
    triangles = _triangulate_points(points)

    # 5) Encodage final Triangles
    return _encode_triangles(points, triangles)
