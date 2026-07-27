from enum import Enum


class IntentType(str, Enum):

    PRODUCT_SEARCH = "product_search"

    STOCK_CHECK = "stock_check"

    ORDER_CREATE = "order_create"

    ORDER_STATUS = "order_status"

    FAQ = "faq"

    OFFER = "offer"

    UNKNOWN = "unknown"



class IntentRouter:


    def detect_intent(self, query: str):

        query = query.lower()


        if any(
            word in query
            for word in [
                "price",
                "cost",
                "rate",
                "buy",
                "need"
            ]
        ):
            return IntentType.PRODUCT_SEARCH



        elif any(
            word in query
            for word in [
                "stock",
                "available",
                "quantity"
            ]
        ):
            return IntentType.STOCK_CHECK



        elif any(
            word in query
            for word in [
                "order",
                "book",
                "purchase"
            ]
        ):
            return IntentType.ORDER_CREATE



        elif any(
            word in query
            for word in [
                "delivery",
                "status",
                "where"
            ]
        ):
            return IntentType.ORDER_STATUS



        elif any(
            word in query
            for word in [
                "time",
                "open",
                "close",
                "address"
            ]
        ):
            return IntentType.FAQ



        else:

            return IntentType.UNKNOWN