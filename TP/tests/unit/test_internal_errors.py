"""Tests unitaires pour la gestion des erreurs internes dans `core`."""

import uuid

import pytest

from triangulator import core


def test_triangulate_raises_value_error_on_invalid_uuid():
    """Un identifiant de PointSet invalide doit lever ValueError."""

    with pytest.raises(ValueError):
        core.triangulate("not-a-valid-uuid")


def test_triangulate_propagates_not_found(monkeypatch):
    """Une erreur 404 du PointSetManager est propagée en FileNotFoundError."""

    def fake_fetch(_pointset_id: str) -> bytes:  # type: ignore[override]
        raise FileNotFoundError("PointSet not found")

    monkeypatch.setattr(core, "_fetch_pointset_from_manager", fake_fetch)

    with pytest.raises(FileNotFoundError):
        core.triangulate(str(uuid.uuid4()))


def test_triangulate_propagates_unavailable(monkeypatch):
    """Une indisponibilité du PointSetManager se traduit par un RuntimeError."""

    def fake_fetch(_pointset_id: str) -> bytes:  # type: ignore[override]
        raise RuntimeError("Service PointSetManager unavailable")

    monkeypatch.setattr(core, "_fetch_pointset_from_manager", fake_fetch)

    with pytest.raises(RuntimeError):
        core.triangulate(str(uuid.uuid4()))
