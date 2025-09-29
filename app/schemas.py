from pydantic import BaseModel, Field

from typing import Optional 
class ProductBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    stock_quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None


class ProductCreate(ProductBase):
    pass
class ProductUpdate(BaseModel):
    name:str | None
    description:str | None
    stock_quantity:int|None
    low_stock_threshold:int|None


class ProductRead(ProductBase):
    id:int

    class Config:
        orm_mode=True

class StockUpdate(BaseModel):
    quantity: int = Field(..., gt=0) 