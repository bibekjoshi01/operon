from src.base.constants import BaseEnum


class ItemUnits(BaseEnum):
    PCS = "PCS"
    BOX = "BOX"
    STRIP = "STRIP"
    TABLET = "TABLET"
    ML = "ML"
    L = "L"
    G = "G"
    KG = "KG"


class OrderTypes(BaseEnum):
    ORDER = "ORDER"
    RETURN = "RETURN"
