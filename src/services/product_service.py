class ProductService:


    def __init__(self, database=None):
        self.database = database



    def search_product(self, name):

        if self.database:

            products = list(
                self.database.products.find(
                    {
                        "name":
                        {
                            "$regex": name,
                            "$options": "i"
                        }
                    }
                )
            )

            return products


        return []



    def check_stock(self, product_id):

        if self.database:

            product = self.database.products.find_one(
                {
                    "product_id": product_id
                }
            )

            if product:
                return product["stock"]


        return 0
        