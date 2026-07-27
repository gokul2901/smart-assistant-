from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from src.services.notification_service import NotificationService


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


notification_service = NotificationService()



class NotificationRequest(BaseModel):

    customer_name: str

    phone_number: str

    message: str

    channel: str = "whatsapp"



# Send notification

@router.post("/send")
async def send_notification(
    request: NotificationRequest
):

    try:

        result = await notification_service.send(
            customer_name=request.customer_name,
            phone_number=request.phone_number,
            message=request.message,
            channel=request.channel
        )


        return {

            "status": "success",

            "message":
                "Notification sent successfully",

            "data": result

        }


    except Exception as error:


        raise HTTPException(

            status_code=500,

            detail=str(error)

        )



# Send order confirmation

@router.post("/order-confirmation")
async def order_confirmation(
    order_id: str,
    customer_phone: str,
    customer_name: str
):


    message = f"""

Hello {customer_name},

Your order has been confirmed.

Order ID: {order_id}

Thank you for shopping with us.

"""


    result = await notification_service.send(
        customer_name=customer_name,
        phone_number=customer_phone,
        message=message,
        channel="whatsapp"
    )


    return {

        "status": "sent",

        "order_id": order_id,

        "result": result

    }



# Send order status update

@router.post("/order-status")
async def order_status_update(
    order_id: str,
    status: str,
    customer_phone: str
):


    message = f"""

Your order status has been updated.

Order ID: {order_id}

Current Status: {status}

"""


    result = await notification_service.send(
        customer_name="Customer",
        phone_number=customer_phone,
        message=message,
        channel="whatsapp"
    )


    return {

        "status": "sent",

        "order_id": order_id,

        "result": result

    }