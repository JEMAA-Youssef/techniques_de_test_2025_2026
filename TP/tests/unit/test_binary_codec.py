import pytest
from triangulator import binary_utils

def test_encode_pointset_placeholder():
    """Test placeholder - vérifier l'encodage binaire d'un PointSet."""
    with pytest.raises(NotImplementedError):
        binary_utils.encode_pointset([])  # pas encore implémenté
