from src.rag.intent_router import IntentRouter



def test_product_query():

    router = IntentRouter()


    intent = router.detect_intent(
        "What is the price of tomato?"
    )


    assert (
        intent.value
        ==
        "product_search"
    )



def test_faq_query():

    router = IntentRouter()


    intent = router.detect_intent(
        "What time does shop open?"
    )


    assert (
        intent.value
        ==
        "faq"
    )