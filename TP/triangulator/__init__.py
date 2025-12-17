"""Package du micro-service Triangulator.

Ce package contient :

* la logique de calcul de triangulation (``core``) ;
* les fonctions d'encodage/décodage binaire (``binary_utils``) ;
* l'API Flask exposant le service (``api``).
"""

from .core import triangulate  # noqa: F401

__all__ = ["triangulate"]
