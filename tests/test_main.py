from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_root_returns_success():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_when_dependencies_are_available(monkeypatch):
    monkeypatch.setattr(main, "check_database", lambda: True)
    monkeypatch.setattr(main, "check_redis", lambda: True)

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "services": {"database": "ok", "redis": "ok"},
    }


def test_health_when_database_is_unavailable(monkeypatch):
    def fail():
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(main, "check_database", fail)
    monkeypatch.setattr(main, "check_redis", lambda: True)

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "error"
    assert response.json()["services"]["database"] == "error"
