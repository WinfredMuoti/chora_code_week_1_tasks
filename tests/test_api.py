import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import api
from fastapi import FastAPI

@pytest.fixture(autouse=True)
def clean_data(tmp_path, monkeypatch):
    test_data = tmp_path / "tasks.json"
    monkeypatch.setattr(api, "DATA", test_data)
    
@pytest.fixture
def client():
    return TestClient(api.app)
#client = TestClient(api.app)

def test_list_is_initially_empty(client):
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == {"tasks": []}

def test_create_then_list(client):
    response = client.post("/tasks", json={"title": "Buy milk"})
    assert response.status_code == 201
    assert response.json()["title"] == "Buy milk"
    listed = client.get("/tasks").json()["tasks"]
    assert len(listed) == 1

def test_create_without_title_returns_400(client):
    r = client.post("/tasks", json={})
    assert r.status_code == 400
    
def test_get_task_happy_path(client):
    created = client.post("/tasks", json={"title": "Buy milk"}).json()
    task_id = created["id"]
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 200
    
def test_get_task_404(client):
    r = client.get("/tasks/999")
    assert r.status_code == 404
    
def test_complete_task_happy_path(client):
    created = client.post("/tasks", json={"title": "Buy milk"}).json()
    task_id = created["id"]
    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200

def test_complete_task_404(client):
    r = client.patch("/tasks/999/complete")
    assert r.status_code == 404
    
def test_delete_task_happy_path(client):
    created = client.post("/tasks", json={"title": "Buy milk"}).json()
    task_id = created["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    
def test_delete_task_404(client):
    r = client.delete("/tasks/999")
    assert r.status_code == 404                        
