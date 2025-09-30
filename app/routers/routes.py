from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import models
from app import schemas

from app.db.database import get_db
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.post("/products", response_model=schemas.ProductRead)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Products(
        name=product.name,
        description=product.description,
        stock_quantity=product.stock_quantity,
        low_stock_threshold=product.low_stock_threshold
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    logging.info(f"Created product {db_product.name}")
    return db_product

@router.get("/products", response_model=list[schemas.ProductRead])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    logging.info("Fetched all products")
    return products

@router.get("/products/low-stock-alert", response_model=list[schemas.ProductRead])
def low_stock_alert(db: Session = Depends(get_db)):
    products = db.query(models.Products)\
                 .filter(models.Products.stock_quantity <= models.Products.low_stock_threshold)\
                 .all()
    logging.info(f"Fetched {len(products)} low-stock products")
    return products


@router.get("/products/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=schemas.ProductRead)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Products).filter(models.Products.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.name is not None:
        db_product.name = product.name
    if product.description is not None:
        db_product.description = product.description
    if product.stock_quantity is not None:
        db_product.stock_quantity = product.stock_quantity
    if product.low_stock_threshold is not None:
        db_product.low_stock_threshold = product.low_stock_threshold

    db.commit()
    db.refresh(db_product)
    logging.info(f"Updated product ID {product_id}")
    return db_product


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Products).filter(models.Products.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    logging.info(f"Deleted product ID {product_id}")
    return {"detail": "Product deleted successfully"}


@router.post("/products/increasing-stock/{product_id}", response_model=schemas.ProductRead)
def increase_stock(product_id: int, stock: schemas.StockUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Products).filter(models.Products.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.stock_quantity += stock.quantity
    db.commit()
    db.refresh(db_product)
    return db_product


@router.post("/products/decreasing-stock/{product_id}", response_model=schemas.ProductRead)
def decrease_stock(product_id: int, stock: schemas.StockUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Products).filter(models.Products.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    if db_product.stock_quantity < stock.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    db_product.stock_quantity -= stock.quantity
    db.commit()
    db.refresh(db_product)
    return db_product




