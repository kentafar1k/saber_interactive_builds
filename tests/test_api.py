import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_tasks_success(monkeypatch):
    class DummyService:
        def get_sorted_tasks(self, build_name):
            assert build_name == "build1"
            return ["a", "b"]
    monkeypatch.setattr("app.core.config.build_service", DummyService())
    response = client.post("/api/v1/get_tasks", json={"build": "build1"})
    assert response.status_code == 200
    assert response.json() == ["a", "b"]

def test_get_tasks_not_found(monkeypatch):
    class DummyService:
        def get_sorted_tasks(self, build_name):
            raise ValueError("Build 'not_exist' not found")
    monkeypatch.setattr("app.core.config.build_service", DummyService())
    response = client.post("/api/v1/get_tasks", json={"build": "not_exist"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_get_tasks_cycle(monkeypatch):
    class DummyService:
        def get_sorted_tasks(self, build_name):
            raise RuntimeError("Cyclic dependency detected at 'a'")
    monkeypatch.setattr("app.core.config.build_service", DummyService())
    response = client.post("/api/v1/get_tasks", json={"build": "build1"})
    assert response.status_code == 422
    assert "Cyclic" in response.json()["detail"] 