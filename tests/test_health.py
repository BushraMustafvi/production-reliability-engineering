from fastapi.testclient import TestClient

from application.api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ready():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {"version": "0.1.0"}
