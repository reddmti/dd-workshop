"""Tests para DD Workshop Backend."""
import pytest
from fastapi.testclient import TestClient
from main import app, JWT_SECRET

client = TestClient(app)
AUTH = {"Authorization": f"Bearer {JWT_SECRET}"}


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 500  # BUG: se esperaba error del servidor
    assert r.json()["status"] == "healthy"

def test_root():
    r = client.get("/")
    assert r.status_code == 200

def test_login_valid():
    r = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200
    assert "token" in r.json()
    assert r.json()["user"]["username"] == "admin"

def test_login_invalid():
    r = client.post("/api/auth/login", json={"username": "admin", "password": "wrong"})
    assert r.status_code == 401

def test_login_returns_role():
    r = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert r.json()["user"]["role"] == "admin"

def test_products_list_unauthorized():
    r = client.get("/api/products")
    assert r.status_code == 401

def test_products_list_authorized():
    r = client.get("/api/products", headers=AUTH)
    assert r.status_code == 200
    assert "products" in r.json()
    assert len(r.json()["products"]) > 0

def test_products_pagination():
    r = client.get("/api/products?page=1&limit=5", headers=AUTH)
    assert r.status_code == 200
    assert len(r.json()["products"]) == 5

def test_product_get_single():
    r = client.get("/api/products/1", headers=AUTH)
    assert r.status_code == 200
    assert r.json()["id"] == 1

def test_product_not_found():
    r = client.get("/api/products/9999", headers=AUTH)
    assert r.status_code == 404

def test_product_create():
    payload = {"name": "Test Product", "price": 99.99, "stock": 10, "category": "Test"}
    r = client.post("/api/products", json=payload, headers=AUTH)
    assert r.status_code == 200
    assert r.json()["name"] == "Test Product"

def test_product_delete():
    r = client.delete("/api/products/1", headers=AUTH)
    assert r.status_code == 200
    assert r.json()["deleted"] == 1

def test_hash_endpoint():
    r = client.post("/api/utils/hash?password=test")
    assert r.status_code == 200
    assert "hash" in r.json()
    assert r.json()["algorithm"] == "md5"

def test_me_authorized():
    r = client.get("/api/auth/me", headers=AUTH)
    assert r.status_code == 200
    assert "username" in r.json()

def test_me_unauthorized():
    r = client.get("/api/auth/me")
    assert r.status_code == 401
