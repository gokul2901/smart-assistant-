import re



class Validators:


    @staticmethod
    def validate_phone(
        phone: str
    ):

        """
        Validate Indian mobile number
        """

        pattern = r"^[6-9]\d{9}$"


        return bool(
            re.match(
                pattern,
                phone
            )
        )



    @staticmethod
    def validate_email(
        email: str
    ):

        pattern = (
            r"^[\w\.-]+@[\w\.-]+\.\w+$"
        )


        return bool(
            re.match(
                pattern,
                email
            )
        )



    @staticmethod
    def validate_quantity(
        quantity:int
    ):

        """
        Product quantity validation
        """

        return quantity > 0



    @staticmethod
    def validate_price(
        price:float
    ):

        return price >= 0