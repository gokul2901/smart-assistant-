from fastapi import APIRouter, HTTPException

from src.services.order_service import OrderService
from src.models.order import Order


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


order_service = OrderService()


# Create new order

@router.post("/")
async def create_order(
    order: Order
):

    result = await order_service.create_order(
        order
    )

    return {
        "status": "success",
        "message": "Order created successfully",
        "order": result
    }



# Get order by ID

@router.get("/{order_id}")
async def get_order(
    order_id: str
):

    order = await order_service.get_order_by_id(
        order_id
    )


    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )


    return {
        "status": "success",
        "order": order
    }



# Get customer orders

@router.get("/customer/{customer_id}")
async def get_customer_orders(
    customer_id: str
):

    orders = await order_service.get_customer_orders(
        customer_id
    )


    return {
        "status": "success",
        "customer_id": customer_id,
        "orders": orders
    }



# Track order status

@router.get("/{order_id}/status")
async def track_order(
    order_id: str
):

    status = await order_service.get_order_status(
        order_id
    )


    if not status:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )


    return {
        "order_id": order_id,
        "status": status
    }



# Update order status (Admin)

@router.put("/{order_id}/status")
async def update_order_status(
    order_id: str,
    status: str
):

    result = await order_service.update_status(
        order_id,
        status
    )


    if not result:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )


    return {
        "status": "updated",
        "order": result
    }



# Cancel order

@router.put("/{order_id}/cancel")
async def cancel_order(
    order_id: str
):

    result = await order_service.cancel_order(
        order_id
    )


    if not result:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )


    return {
        "status": "cancelled",
        "order": result
    }