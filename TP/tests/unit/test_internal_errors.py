import pytest
from triangulator import core

def test_internal_error_handling():
    """Vérifie la gestion d'une erreur interne."""
    with pytest.raises(NotImplementedError):
        core.triangulate("invalid_input")
