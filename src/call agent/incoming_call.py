# src/call_agent/incoming_call.py

from fastapi import APIRouter, Request

from src.call_agent.call_manager import CallManager


router = APIRouter(
    prefix="/call",
    tags=["Voice Call"]
)


call_manager = CallManager()



@router.post("/incoming")
async def incoming_call(
    request: Request
):

    data = await request.json()


    call_id = data.get(
        "call_id"
    )

    phone = data.get(
        "phone"
    )


    call_manager.start_call(
        call_id,
        phone
    )


    return {

        "message":
        "Welcome to Gokul Departmental Store",

        "call_id":
        call_id

    }