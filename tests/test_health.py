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
    assert response.json() == {"version": "0.2.0"}


def test_create_order():
    response = client.post(
        "/orders",
        json={
            "order_id": "ORD-TEST-001",
            "customer_id": "CUS-TEST-001",
            "amount": 149.99,
            "currency": "USD",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "order_id": "ORD-TEST-001",
        "customer_id": "CUS-TEST-001",
        "amount": 149.99,
        "currency": "USD",
        "status": "created",
    }


def test_get_order():
    response = client.get("/orders/ORD-TEST-001")

    assert response.status_code == 200
    assert response.json()["order_id"] == "ORD-TEST-001"


def test_missing_order():
    response = client.get("/orders/DOES-NOT-EXIST")

    assert response.status_code == 404
    assert response.json() == {"detail": "order not found"}


def test_duplicate_order():
    response = client.post(
        "/orders",
        json={
            "order_id": "ORD-DUPLICATE",
            "customer_id": "CUS-001",
            "amount": 50.00,
            "currency": "USD",
        },
    )

    assert response.status_code == 201

    duplicate = client.post(
        "/orders",
        json={
            "order_id": "ORD-DUPLICATE",
            "customer_id": "CUS-002",
            "amount": 75.00,
            "currency": "USD",
        },
    )

    assert duplicate.status_code == 409
    assert duplicate.json() == {"detail": "order already exists"}


def test_invalid_amount():
    response = client.post(
        "/orders",
        json={
            "order_id": "ORD-INVALID",
            "customer_id": "CUS-001",
            "amount": 0,
            "currency": "USD",
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "amount must be greater than zero"
    }
