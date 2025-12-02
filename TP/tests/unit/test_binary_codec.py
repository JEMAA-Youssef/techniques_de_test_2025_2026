import pytest
from triangulator import binary_utils

def test_encode_pointset_not_implemented():
    """Vérifie que l'encodage binaire n'est pas encore implémenté."""
    with pytest.raises(NotImplementedError):
        binary_utils.encode_pointset([])

def test_decode_pointset_not_implemented():
    """Vérifie que le décodage binaire n'est pas encore implémenté."""
    with pytest.raises(NotImplementedError):
        binary_utils.decode_pointset(b"")
