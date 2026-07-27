from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    """
    Type of notification
    """

    order_confirmation = "order_confirmation"
    order_status = "order_status"
    delivery_update = "delivery_update"
    low_stock_alert = "low_stock_alert"
    offer_alert = "offer_alert"
    admin_alert = "admin_alert"



class NotificationChannel(str, Enum):
    """
    Notification sending method
    """

    whatsapp = "whatsapp"
    sms = "sms"
    email = "email"
    app = "app"



class NotificationStatus(str, Enum):
    """
    Notification delivery status
    """

    pending = "pending"
    sent = "sent"
    delivered = "delivered"
    failed = "failed"



class Notification(BaseModel):
    """
    Notification model
    """

    notification_id: Optional[str] = None


    user_id: Optional[str] = None

    customer_phone: Optional[str] = None


    order_id: Optional[str] = None


    notification_type: NotificationType


    channel: NotificationChannel


    title: str


    message: str


    status: NotificationStatus = NotificationStatus.pending


    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )


    sent_at: Optional[datetime] = None