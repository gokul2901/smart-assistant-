from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Supplier(BaseModel):
    """
    Supplier information model
    """

    supplier_id: Optional[str] = None

    supplier_name: str

    company_name: Optional[str] = None

    category: Optional[str] = None


    phone_number: str

    email: Optional[str] = None


    address: Optional[str] = None


    city: Optional[str] = None


    products_supplied: Optional[list[str]] = []


    payment_terms: Optional[str] = None
    # Example:
    # "30 days credit"


    gst_number: Optional[str] = None


    is_active: bool = True


    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )