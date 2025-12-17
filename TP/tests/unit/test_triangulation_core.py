"""Tests unitaires pour la logique de triangulation."""

import uuid

import pytest

from triangulator import core, binary_utils


def test_triangulate_points_triangle():
    """Trois points forment exactement un triangle."""

    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = core._triangulate_points(points)

    assert triangles == [(0, 1, 2)]


def test_triangulate_points_square_two_triangles():
    """Un carré est triangulé en deux triangles en éventail."""

    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = core._triangulate_points(points)

    assert triangles == [(0, 1, 2), (0, 2, 3)]


def test_triangulate_points_less_than_three_points():
    """Moins de trois points ne permet pas de former de triangle."""

    assert core._triangulate_points([]) == []
    assert core._triangulate_points([(0.0, 0.0)]) == []
    assert core._triangulate_points([(0.0, 0.0), (1.0, 0.0)]) == []


def test_triangulate_full_flow_encodes_triangles(monkeypatch):
    """`triangulate` renvoie un binaire Triangles conforme après récupération du PointSet."""

    # Points formant un carré → deux triangles attendus via l'algorithme en éventail.
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    pointset_binary = binary_utils.encode_pointset(points)

    def fake_fetch(_pointset_id: str) -> bytes:
        return pointset_binary

    monkeypatch.setattr(core, "_fetch_pointset_from_manager", fake_fetch)

    pointset_id = str(uuid.uuid4())
    result = core.triangulate(pointset_id)

    # La première partie doit être exactement le PointSet encodé.
    assert result.startswith(pointset_binary)

    # On vérifie ensuite l'en-tête nombre de triangles.
    import struct

    triangles_header = result[len(pointset_binary) : len(pointset_binary) + 4]
    (triangle_count,) = struct.unpack(">I", triangles_header)

    assert triangle_count == 2
