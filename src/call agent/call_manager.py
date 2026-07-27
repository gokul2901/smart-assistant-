# src/call_agent/call_manager.py

from loguru import logger


class CallManager:

    def __init__(self):
        self.active_calls = {}


    def start_call(
        self,
        call_id,
        phone_number
    ):

        self.active_calls[call_id] = {

            "phone": phone_number,
            "status": "active",
            "conversation": []

        }


        logger.info(
            f"Call started {call_id}"
        )


        return self.active_calls[call_id]



    def add_message(
        self,
        call_id,
        role,
        message
    ):

        self.active_calls[call_id]["conversation"].append({

            "role": role,
            "message": message

        })



    def end_call(
        self,
        call_id
    ):

        self.active_calls[call_id]["status"] = "completed"


        logger.info(
            f"Call ended {call_id}"
        )


        return self.active_calls[call_id]



    def get_call(
        self,
        call_id
    ):

        return self.active_calls.get(call_id)