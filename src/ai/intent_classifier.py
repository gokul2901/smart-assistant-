from typing import Dict


class IntentClassifier:
    """
    Customer query intent detection
    Used before RAG and order processing
    """

    INTENTS = {

        "product_search": [
            "available",
            "have",
            "price",
            "cost",
            "product",
            "item"
        ],

        "stock_check": [
            "stock",
            "available",
            "quantity",
            "left"
        ],

        "create_order": [
            "order",
            "buy",
            "want",
            "need",
            "give me"
        ],

        "order_status": [
            "status",
            "where",
            "track",
            "delivery"
        ],

        "offer_query": [
            "offer",
            "discount",
            "sale",
            "deal"
        ],

        "store_info": [
            "timing",
            "open",
            "close",
            "address",
            "location"
        ],

        "complaint": [
            "problem",
            "issue",
            "wrong",
            "complaint"
        ],

        "general_chat": [
            "hello",
            "hi",
            "thank",
            "help"
        ]
    }


    @staticmethod
    def classify(query: str) -> Dict:

        query = query.lower().strip()


        scores = {}

        for intent, keywords in IntentClassifier.INTENTS.items():

            score = 0

            for keyword in keywords:

                if keyword in query:
                    score += 1

            scores[intent] = score


        best_intent = max(
            scores,
            key=scores.get
        )


        confidence = scores[best_intent]


        if confidence == 0:
            return {
                "intent": "unknown",
                "confidence": 0
            }


        return {
            "intent": best_intent,
            "confidence": confidence
        }


if __name__ == "__main__":
    sample_queries = [
        "Do you have stock for milk?",
        "I want to buy 2 chocolates",
        "Where is your store located?",
        "What is the status of my order?",
        "Any discounts or offers today?",
        "Hello, good morning!"
    ]

    print("--- Intent Classifier Verification ---")
    for q in sample_queries:
        res = IntentClassifier.classify(q)
        print(f"Query: '{q}' -> Intent: {res['intent']} (Confidence: {res['confidence']})")