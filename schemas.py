from pydantic import BaseModel
from typing import Optional


class ProductSchema(BaseModel):
    name: str
    url: str
    store_id: str
    sku: str
    brand: str
    category: str
    descriptions: str
    images: str


class PriceSchema(BaseModel):
    price: str
    product_id: Optional[int]
    discount: str = '0'
