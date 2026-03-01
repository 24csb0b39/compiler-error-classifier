import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "🚀 Compiler Error Classifier API v1.0"

def test_analyze_valid_code():
    response = client.post("/analyze", json={"code": "int main(){return 0;}"})
    assert response.status_code == 200
    assert "ml_predictions" in response.json()

def test_analyze_error_code():
    buggy = 'int x = "hello"; y = 5;'
    response = client.post("/analyze", json={"code": buggy})
    assert response.status_code == 200
    data = response.json()
    assert "SEM001" in str(data) or "SEM002" in str(data)
