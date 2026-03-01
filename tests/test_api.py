import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "ML Compiler API" in response.json()["message"]  # FIXED

def test_analyze_valid_code():
    response = client.post("/analyze", json={"code": "int main(){return 0;}"})
    assert response.status_code == 200
    assert "predictions" in response.json()  # FIXED: ml_predictions → predictions

def test_analyze_error_code():
    buggy = 'int x = "hello";'
    response = client.post("/analyze", json={"code": buggy})
    assert response.status_code == 200
    data = response.json()
    assert data["error_count"] >= 1
    assert "predictions" in data
