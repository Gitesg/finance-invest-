from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine
from sqlalchemy.orm import Session

client = TestClient(app)

def test_increase_stock():
    # Create product first
    response = client.post("/products", json={
        "name": "Test Product",
        "description": "Test",
        "stock_quantity": 10,
        "low_stock_threshold": 5
    })
    product = response.json()
    product_id = product["id"]

    # Increase stock
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
    product = response.json()
    product_id = product["id"]

    # Try to remove more than available
    response = client.post(f"/products/decreasing-stock/{product_id}", json={"quantity": 10})
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient stock"

def test_low_stock_endpoint():
    # Create a product below threshold
    response = client.post("/products", json={
        "name": "Low Stock Product",
        "description": "Test",
        "stock_quantity": 2,
        "low_stock_threshold": 5
    })
    response = client.get("/products/low-stock")
    products = response.json()
    assert any(p["name"] == "Low Stock Product" for p in products)
