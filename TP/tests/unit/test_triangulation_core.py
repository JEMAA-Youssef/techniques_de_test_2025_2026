import pytest
from triangulator import core

def test_triangulation_algorithm_placeholder():
    """Vérifie que la fonction de triangulation existe."""
    with pytest.raises(NotImplementedError):
        core.triangulate([])
