class SupplierService:


    def __init__(self, database=None):

        self.database = database



    def add_supplier(
        self,
        supplier_data
    ):


        if self.database:

            self.database.suppliers.insert_one(
                supplier_data
            )


        return supplier_data



    def get_supplier(
        self,
        supplier_id
    ):


        if self.database:

            return self.database.suppliers.find_one(
                {
                    "supplier_id":
                    supplier_id
                }
            )


        return None