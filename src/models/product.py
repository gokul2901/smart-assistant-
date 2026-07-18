from pydantic import BaseModel

class Product(BaseModel):
    product_id: str
    name: str
    category: str
    price: float
    stock: int