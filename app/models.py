from sqlalchemy import TIMESTAMP, Column, Integer, Numeric, String, text
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String, nullable=False, index=True)
    price = Column(Numeric(6, 2), nullable=False)
    brand = Column(String, nullable=True)
    portfolio = Column(String, nullable=True)
    volume = Column(Numeric, nullable=True)
    GTIN = Column(String(14), nullable=True, index=True)
    SKU = Column(String, nullable=True, index=True)
    pack_size = Column(Integer, nullable=True)
    stock_quantity = Column(Integer, nullable=False)
    resource_identifier = Column(String, nullable=False)
    date_added = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))