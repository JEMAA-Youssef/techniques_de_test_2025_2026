import pytest

@pytest.mark.performance
def test_triangulation_performance_placeholder(benchmark):
    """Test de performance placeholder."""
    def fake_triangulation():
        return []
    result = benchmark(fake_triangulation)
    assert result == []
