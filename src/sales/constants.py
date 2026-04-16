from src.base.constants import BaseEnum


class PayTypes(BaseEnum):
    CASH = "CASH"
    CREDIT = "CREDIT"


class SaleTypes(BaseEnum):
    SALE = "SALE"
    RETURN = "RETURN"
