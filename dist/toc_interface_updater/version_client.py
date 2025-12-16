"""Wago API client for fetching version information."""

from typing import TypedDict

import requests

from .toc_types import Product, VersionCache, is_valid_product


class BuildInfo(TypedDict):
    product: str
    version: str
    created_at: str
    build_config: str
    product_config: str
    cdn_config: str


def product_version(req_product: Product, version_cache: VersionCache) -> str:
    """Fetch the latest builds information from Wago API."""
    if req_product in version_cache:
        return version_cache[req_product]

    url = "https://wago.tools/api/builds/latest"
    product_map = {}
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        product_map: dict[str, BuildInfo] = response.json()
    except requests.RequestException as e:
        print(f"Error communicating with server: {e}")
        return "00000"

    for product, build_info in product_map.items():
        if not is_valid_product(product) and product not in version_cache:
            print(
                f"Warning: Received unknown product '{product}' from API, skipping for now. Please open an issue if this product is valid."
            )
            continue

        product_key = Product(product)
        version_parts = build_info.get("version").split(".")[:3]
        major = version_parts[0]
        minor = version_parts[1].zfill(2)  # Ensure minor is 2 digits
        patch = version_parts[2].zfill(2)  # Ensure patch is 2 digits
        version_cache[product_key] = f"{major}{minor}{patch}"

    return version_cache[req_product]
