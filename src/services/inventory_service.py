def check_stock(product):

    if product["stock"] < 10:
        return "Low Stock"

    return "Available"






#     CSV Product Data
#         │
#         ▼
# inventory_service.py
#         │
#         ▼
# check_stock(product)
#         │
#         ▼
# Read Stock Value
#         │
#         ▼
# Stock < 10 ?
#      /     \
#    Yes      No
#     │        │
#     ▼        ▼