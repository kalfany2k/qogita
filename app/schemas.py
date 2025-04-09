from typing import Optional
from pydantic import BaseModel, field_validator

class Input(BaseModel):
    product_name: str
    GTIN: Optional[str] = None
    price: float
    stock_quantity: int
    pack_size: Optional[int] = None

    # Sanitize empty fields because "" is not considered a null value in the CSV
    @field_validator('GTIN', 'pack_size', mode='before')
    def from_str_to_None(cls, v: str):
        return None if v == "" else v
    
    @field_validator('GTIN')
    def check_GTIN_size(cls, v):
        if v is not None:
            if len(v) in [8, 12, 13, 14]:
                return v
            else:
                raise ValueError("GTIN can only be 8, 12, 13 or 14 digits long.")
    def check_GTIN_numerical(cls, v):
        if v is not None and int(v):
            return v
        
        raise ValueError("GTIN can only be a numerical value.")

class CSVInput(Input):
    SKU: str

class XMLInput(Input):
    brand: str
    portfolio: str
    volume: int