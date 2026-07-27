import pandas as pd
import re
from loguru import logger


class DataValidator:

    REQUIRED_COLUMNS = [
        "Product ID",
        "Category",
        "Product Name",
        "Brand",
        "Price",
        "Stock"
    ]

    @staticmethod
    def validate_required_columns(df: pd.DataFrame):
        missing_columns = [
            col for col in DataValidator.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        logger.info("Required columns validation passed")

    @staticmethod
    def remove_duplicates(df: pd.DataFrame):
        before = len(df)

        df = df.drop_duplicates()

        after = len(df)

        logger.info(
            f"Removed {before - after} duplicate rows"
        )

        return df

    @staticmethod
    def validate_prices(df: pd.DataFrame):
        invalid_prices = df[
            (df["Price"].isna()) |
            (df["Price"] <= 0)
        ]

        logger.info(
            f"Invalid price rows: {len(invalid_prices)}"
        )

        return invalid_prices

    @staticmethod
    def validate_stock(df: pd.DataFrame):
        invalid_stock = df[
            (df["Stock"].isna()) |
            (df["Stock"] < 0)
        ]

        logger.info(
            f"Invalid stock rows: {len(invalid_stock)}"
        )

        return invalid_stock

    @staticmethod
    def validate_email(email):
        if pd.isna(email):
            return False

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        return bool(re.match(pattern, str(email)))

    @staticmethod
    def validate_phone(phone):
        if pd.isna(phone):
            return False

        phone = str(phone).strip()

        return phone.isdigit() and len(phone) >= 10

    @staticmethod
    def clean_text_fields(df: pd.DataFrame):

        text_columns = df.select_dtypes(
            include=["object"]
        ).columns

        for col in text_columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

        logger.info("Text fields cleaned")

        return df

    @staticmethod
    def validate_supplier_data(df: pd.DataFrame):

        if "Supplier Email" in df.columns:

            invalid_email_count = (
                ~df["Supplier Email"]
                .apply(DataValidator.validate_email)
            ).sum()

            logger.info(
                f"Invalid supplier emails: "
                f"{invalid_email_count}"
            )

        if "Supplier Phone" in df.columns:

            invalid_phone_count = (
                ~df["Supplier Phone"]
                .apply(DataValidator.validate_phone)
            ).sum()

            logger.info(
                f"Invalid supplier phones: "
                f"{invalid_phone_count}"
            )

    @staticmethod
    def validate_dataframe(df: pd.DataFrame):

        logger.info("Starting validation")

        DataValidator.validate_required_columns(df)

        df = DataValidator.clean_text_fields(df)

        df = DataValidator.remove_duplicates(df)

        invalid_prices = (
            DataValidator.validate_prices(df)
        )

        invalid_stock = (
            DataValidator.validate_stock(df)
        )

        DataValidator.validate_supplier_data(df)

        report = {
            "total_rows": len(df),
            "invalid_price_rows": len(invalid_prices),
            "invalid_stock_rows": len(invalid_stock)
        }

        logger.info(f"Validation Report: {report}")

        return df, report