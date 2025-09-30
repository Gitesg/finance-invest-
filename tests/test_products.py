# tests/test_products.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app
from app.db.database import engine
import logging



client = TestClient(app)
logging.basicConfig(level=logging.INFO)

@pytest.fixture(autouse=True)
def clean_db():
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE;"))
    yield


def test_increase_stock():
    
    response = client.post("/products", json={
        "name": "Test Product",
        "description": "Test",
        "stock_quantity": 10,
        "low_stock_threshold": 5
    })
    assert response.status_code == 200
    product = response.json()
    product_id = product["id"]

   
    response = client.post(f"/products/increasing-stock/{product_id}", json={"quantity": 5})
    assert response.status_code == 200
    assert response.json()["stock_quantity"] == 15


def test_decrease_stock_insufficient():
    response = client.post("/products", json={
        "name": "Test Product 2",
        "description": "Test",
        "stock_quantity": 5,
        "low_stock_threshold": 2
    })
    assert response.status_code == 200
    product = response.json()
    product_id = product["id"]

    response = client.post(f"/products/decreasing-stock/{product_id}", json={"quantity": 10})
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient stock"


def test_low_stock_endpoint():
    
    response = client.post("/products", json={
        "name": "Low Stock Product",
        "description": "Test",
        "stock_quantity": 2,
        "low_stock_threshold": 5
    })
    logging.info(response.json())   
    logging.info(response.status_code)
    logging.info("Created product for low stock test")
    assert response.status_code == 200

    response = client.get("/products/low-stock-alert")
    assert response.status_code == 200
    products = response.json()
    assert any(p["name"] == "Low Stock Product" for p in products)
