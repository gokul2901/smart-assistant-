from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    """
    Order status tracking
    """

    pending = "pending"
    confirmed = "confirmed"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    completed = "completed"
    cancelled = "cancelled"



class OrderItem(BaseModel):
    """
    Individual product inside an order
    """

    product_id: str
    product_name: str
    quantity: int = Field(gt=0)
    price: float
    total_price: float



class DeliveryType(str, Enum):

    takeaway = "takeaway"
    delivery = "delivery"



class Order(BaseModel):
    """
    Customer order model
    """

    order_id: Optional[str] = None

    customer_id: Optional[str] = None

    customer_name: str

    phone_number: str

    items: List[OrderItem]


    total_amount: float


    delivery_type: DeliveryType


    delivery_address: Optional[str] = None


    status: OrderStatus = OrderStatus.pending


    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )