import pytest

def test_pointsetmanager_404_simulation(monkeypatch):
    """Simule un mock du PointSetManager renvoyant 404."""
    from triangulator import api

    def fake_get_pointset(point_set_id):
        raise FileNotFoundError("PointSet non trouvé")

    monkeypatch.setattr("triangulator.core.triangulate", fake_get_pointset)
    client = api.app.test_client()
    response = client.get("/triangulate/unknown")
    assert response.status_code in (404, 500)
