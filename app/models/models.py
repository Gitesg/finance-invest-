

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy.sql import func


class Products(Base):
    __tablename__="products"
    id=Column(Integer,primary_key=True,index=True,nullable=False,autoincrement=True)
    name=Column(String,nullable=False)
    description=Column(String,nullable=False)
    stock_quantity=Column(Integer,nullable=False)
    low_stock_threshold=Column(Integer,nullable=False)
