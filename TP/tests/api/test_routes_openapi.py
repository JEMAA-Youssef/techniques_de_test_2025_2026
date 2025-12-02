import pytest

# Données simulées
IDS = ["00000000-0000-0000-0000-000000000001"]
TRIANGLES = {IDS[0]: b"\x00\x00\x00\x00"}
MALFORMED_ID = "not-a-valid-uuid"
UNKNOWN_ID = "99999999-9999-9999-9999-999999999999"

def mocked_get_and_compute(point_set_id: str) -> bytes:
    if point_set_id in IDS:
        return TRIANGLES[point_set_id]
    else:
        raise KeyError("Point set ID not found")

def mocked_get_and_compute_failed(point_set_id: str) -> bytes:
    raise Exception("Computation failed")

def mocked_get_and_compute_no_service(point_set_id: str) -> bytes:
    raise RuntimeError("Service not available")

ENDPOINT = "/triangulate/{point_set_id}"

@pytest.fixture
def client():
    from triangulator.api import app
    app.testing = True
    with app.test_client() as client:
        yield client

def test_triangulation_valid_id(client, monkeypatch):
    test_id = IDS[0]
    expected_response = TRIANGLES[test_id]
    monkeypatch.setattr("triangulator.core.triangulate", mocked_get_and_compute)
    response = client.get(ENDPOINT.format(point_set_id=test_id))
    assert response.status_code == 200
    assert response.data == expected_response

def test_triangulation_unknown_id(client, monkeypatch):
    monkeypatch.setattr("triangulator.core.triangulate", mocked_get_and_compute)
    response = client.get(ENDPOINT.format(point_set_id=UNKNOWN_ID))
    assert response.status_code == 404

def test_triangulation_malformed_id(client, monkeypatch):
    monkeypatch.setattr("triangulator.core.triangulate", mocked_get_and_compute)
    response = client.get(ENDPOINT.format(point_set_id=MALFORMED_ID))
    assert response.status_code == 400

def test_triangulation_no_id(client, monkeypatch):
    monkeypatch.setattr("triangulator.core.triangulate", mocked_get_and_compute)
    response = client.get("/triangulate/")
    assert response.status_code == 400

def test_triangulation_internal_error(client, monkeypatch):
    test_id = IDS[0]
    monkeypatch.setattr("triangulator.core.triangulate", mocked_get_and_compute_failed)
    response = client.get(ENDPOINT.format(point_set_id=test_id))
    assert response.status_code == 500

def test_triangulation_database_unavailable(client, monkeypatch):
    test_id = IDS[0]
    monkeypatch.setattr("triangulator.core.triangulate", mocked_get_and_compute_no_service)
    response = client.get(ENDPOINT.format(point_set_id=test_id))
    assert response.status_code == 503
