from sqlalchemy import TIMESTAMP, Column, Integer, Numeric, String, text
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String(500), nullable=False, index=True)
    price = Column(Numeric(6, 2), nullable=False)
    brand = Column(String(100), nullable=True)
    portfolio = Column(String(100), nullable=True)
    volume = Column(Numeric(6, 0), nullable=True)
    GTIN = Column(String(14), nullable=True, index=True)
    SKU = Column(String(50), nullable=True, index=True)
    pack_size = Column(Integer, nullable=True)
    stock_quantity = Column(Integer, nullable=False)
    resource_identifier = Column(String(3), nullable=False)
    date_added = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))