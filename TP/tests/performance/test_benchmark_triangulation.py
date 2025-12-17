"""Tests de performance pour la triangulation."""

import pytest

from triangulator import core


@pytest.mark.performance
def test_triangulation_performance_simple(benchmark):
    """Mesure le temps de triangulation sur un nuage de points modéré."""

    # Jeu de 1 000 points disposés sur un cercle.
    import math

    points = [
        (math.cos(i / 10.0), math.sin(i / 10.0)) for i in range(1000)
    ]

    def run_triangulation():
        return core._triangulate_points(points)

    result = benchmark(run_triangulation)

    # On s'assure qu'au moins un triangle est produit.
    assert len(result) > 0
