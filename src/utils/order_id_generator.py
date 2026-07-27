import uuid
from datetime import datetime



class OrderIDGenerator:


    @staticmethod
    def generate():

        """
        Generate unique order ID

        Example:
        ORD-20260725-A1B2C3
        """

        date = datetime.now().strftime(
            "%Y%m%d"
        )

        unique_id = str(uuid.uuid4())[
            :6
        ].upper()


        order_id = (
            f"ORD-{date}-{unique_id}"
        )


        return order_id