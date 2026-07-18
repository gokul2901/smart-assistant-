from pydantic import BaseModel

class Inventory(BaseModel):
    product_id: str
    stock: int