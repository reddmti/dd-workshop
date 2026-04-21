"""Tests básicos para DD Workshop API."""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["version"] == "1.0.0"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_search_user_found():
    response = client.get("/users/search?username=admin")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) > 0
    assert data["users"][0]["username"] == "admin"


def test_search_user_not_found():
    response = client.get("/users/search?username=noexiste")
    assert response.status_code == 404


def test_password_hash():
    response = client.post("/users/password-hash?password=testpass")
    assert response.status_code == 200
    assert "hash" in response.json()
    assert response.json()["algorithm"] == "md5"


def test_login_valid():
    response = client.post("/users/login?username=admin&password=admin123")
    assert response.status_code == 200
    assert "token" in response.json()


def test_login_invalid():
    response = client.post("/users/login?username=admin&password=wrong")
    assert response.status_code == 401
