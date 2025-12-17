"""Tests unitaires pour l'encodage / décodage binaire de PointSet."""

import struct

import pytest

from triangulator import binary_utils


def test_encode_pointset_roundtrip_simple():
    """Un petit ensemble de points se re-décode à l'identique (à l'approximation près)."""

    points = [(0.0, 0.0), (1.5, -2.5)]

    encoded = binary_utils.encode_pointset(points)
    decoded = binary_utils.decode_pointset(encoded)

    assert len(decoded) == len(points)
    for (x_exp, y_exp), (x_got, y_got) in zip(points, decoded):
        assert x_got == pytest.approx(x_exp)
        assert y_got == pytest.approx(y_exp)


def test_encode_pointset_rejects_non_list():
    """L'encodage doit refuser un type autre qu'une liste de tuples."""

    with pytest.raises(ValueError):
        binary_utils.encode_pointset("not-a-list")


def test_decode_pointset_rejects_too_short_buffer():
    """Un buffer plus court que 4 octets est invalide."""

    with pytest.raises(ValueError):
        binary_utils.decode_pointset(b"\x00\x00\x00")


def test_decode_pointset_rejects_incorrect_length():
    """Longueur incohérente entre l'en-tête et la taille réelle du buffer."""

    # Indique 1 point (4 + 8 octets) mais on ne fournit que l'en-tête.
    bogus = struct.pack(">I", 1)

    with pytest.raises(ValueError):
        binary_utils.decode_pointset(bogus)
