from enum import Enum


class OrderStatus(str, Enum):
    """
    Available order statuses
    """

    CREATED = "created"

    CONFIRMED = "confirmed"

    PREPARING = "preparing"

    READY = "ready"

    OUT_FOR_DELIVERY = "out_for_delivery"

    DELIVERED = "delivered"

    CANCELLED = "cancelled"