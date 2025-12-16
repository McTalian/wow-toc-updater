"""Type definitions and enums for the TOC interface updater."""

from enum import Enum
from typing import Dict


class Product(Enum):
    """Enumeration of supported WoW product types."""

    WOW = "wow"
    WOW_BETA = "wow_beta"
    WOW_TEST = "wowt"
    WOW_XPTR = "wowxptr"
    WOW_CLASSIC = "wow_classic"
    WOW_CLASSIC_BETA = "wow_classic_beta"
    WOW_CLASSIC_PTR = "wow_classic_ptr"
    WOW_CLASSIC_ERA = "wow_classic_era"
    # WOW_CLASSIC_ERA_BETA = "wow_classic_era_beta"
    WOW_CLASSIC_ERA_PTR = "wow_classic_era_ptr"


# Product type definitions
VersionCache = Dict[Product, str]


def is_valid_product(product: str) -> bool:
    """Check if a product string is a valid Product type."""
    return Product.__contains__(product)


class GameFlavor(Enum):
    """Enumeration of supported WoW game flavors."""

    WOW = Product.WOW
    WOW_CLASSIC = Product.WOW_CLASSIC
    WOW_CLASSIC_ERA = Product.WOW_CLASSIC_ERA
