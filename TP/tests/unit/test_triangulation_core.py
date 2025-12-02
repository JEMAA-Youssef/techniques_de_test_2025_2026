import pytest
from triangulator import core

def test_triangulate_function_exists():
    """Vérifie que la fonction existe et lève une erreur car non implémentée."""
    with pytest.raises(NotImplementedError):
        core.triangulate([])
