
from fastapi import FastAPI, Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session  

import logging
from app.database import get_db, Base, engine
from app import models, schemas

logging.basicConfig(level=logging.INFO)

router=APIRouter()

@router.get("/products",response_model=list[schemas.ProductRead])
def get_all_products(db:Session=Depends(get_db)):
    products=db.query(models.Products).all()
    logging.info("Fetching all products")
    return products

@router.get("/products/{product_id}",response_model=schemas.ProductRead)
def get_product(product_id:int,db:Session=Depends(get_db)): 
    product=db.query(models.Products).filter(models.Products.id==product_id).first()
    logging.info(f"Fetching product with ID: {product_id}") 
    if not product:
        raise HTTPException(404,detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=schemas.ProductUpdate)
def update_product(product_id:int, product:schemas.ProductUpdate,db:Session=Depends(get_db)):

    db_product=db.query(models.Products).filter(models.Products.id==product_id).first()
    logging.info(f"Updating product with ID: {product_id}")

    if not db_product:
        raise HTTPException(404,detail="Product not found")
    return "helo this is update product"
    

@router.delete("/products/{product_id}")
def delete_product(product_id:int,db:Session=Depends(get_db)):
    db_product=db.query(models.Products).filter(models.Products.id==product_id).first()
    logging.info(f"db_product: {db_product}")
    logging.info(f"Deleting product with ID: {product_id}")
    if not db_product:
        raise HTTPException(404,detail="Product not found")
    try:
        db.delete(db_product)
        db.commit()
        return {"detail":"Product deleted successfully"}  
    except Exception as e:   
        logging.error(f"Error deleting product: {e}")
        raise HTTPException(500,detail="Internal server error")  





@router.post("/products/increasing-stock/{product_id}", response_model=schemas.ProductRead)
def increase_stock(product_id: int, stock: schemas.StockUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Products).filter(models.Products.id == product_id).first()
    if not db_product:
        raise HTTPException(404, detail="Product not found")
    
    
    db_product.stock_quantity += stock.quantity
    db.commit()
    db.refresh(db_product)
    return db_product


@router.post("/products/decreasing-stock/{product_id}", response_model=schemas.ProductRead)
def decrease_stock(product_id: int, stock: schemas.StockUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Products).filter(models.Products.id == product_id).first()
    if not db_product:
        raise HTTPException(404, detail="Product not found")
    
    if db_product.stock_quantity < stock.quantity:
        raise HTTPException(400, detail="Insufficient stock to decrease")
    
    db_product.stock_quantity -= stock.quantity
    db.commit()
    db.refresh(db_product)
    return db_product


@router.post("/products/low-stock-alert/")
def low_stock_alert(db: Session = Depends(get_db)):
    db_products = db.query(models.Products).filter(models.Products.stock_quantity <= models.Products.low_stock_threshold).all()
    if not db_products: 
        return {"detail": "No products are below the low stock threshold"}  
    return db_products



