from src.base.constants import BaseEnum


class MovementTypes(BaseEnum):
    PURCHASE = "PURCHASE"
    SALES = "SALES"
    OPENING_STOCK = "OPENING_STOCK"
    LOST = "LOST"
    DAMAGED = "DAMAGED"
    EXPIRED = "EXPIRED"
    OTHER = "OTHER"
    ADJUSTMENT = "ADJUSTMENT"
