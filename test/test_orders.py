from src.orders.order_manager import OrderManager



def test_create_order():


    manager = OrderManager()


    order = manager.create_order(

        customer_id="CUS001",

        customer_name="Gokul",

        phone_number="9876543210",

        items=[

            {
                "product_id":"P001",

                "product_name":"Tomato",

                "quantity":2,

                "price":40

            }

        ],

        total_amount=80,

        delivery_type="delivery",

        address="Chennai"

    )


    assert "order_id" in order

    assert (
        order["customer_name"]
        ==
        "Gokul"
    )



def test_order_amount():

    amount = 500


    assert amount > 0