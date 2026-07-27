# src/call_agent/outgoing_call.py


from loguru import logger


class OutgoingCall:


    async def make_call(
        self,
        phone_number,
        message
    ):


        logger.info(
            f"Calling {phone_number}"
        )


        return {

            "status":
            "calling",

            "message":
            message

        }