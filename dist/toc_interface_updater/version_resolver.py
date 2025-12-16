"""Version resolution logic for different WoW products."""

import re
from typing import List, Set

from .constants import InterfaceDirective
from .toc_types import VersionCache, Product


def get_beta_products(product: Product) -> List[Product]:
    """Get the list of beta products for a given full product."""
    if product == Product.WOW:
        return [Product.WOW_BETA]
    elif product == Product.WOW_CLASSIC:
        return [Product.WOW_CLASSIC_BETA]
    elif product == Product.WOW_CLASSIC_ERA:
        return []
    return []

def get_test_products(product: Product) -> List[Product]:
    """Get the list of test products for a given full product."""
    if product == Product.WOW:
        return [Product.WOW_TEST, Product.WOW_XPTR]
    elif product == Product.WOW_CLASSIC:
        return [Product.WOW_CLASSIC_PTR]
    elif product == Product.WOW_CLASSIC_ERA:
        return [Product.WOW_CLASSIC_ERA_PTR]
    return []


def detect_existing_versions(
    content: str, product: Product, multi: bool
) -> tuple[Set[str], bool]:
    """
    Detect existing versions from the content and determine if it's single line multi.
    Returns (detected_versions, is_single_line_multi)
    """
    # Check if it's single line multi-version format (comma-separated)
    single_line_pattern = re.compile(
        f"^({re.escape(InterfaceDirective.BASE)}).*\\,.*$", flags=re.MULTILINE
    )
    single_line_multi = bool(single_line_pattern.search(content))

    if single_line_multi:
        single_line_multi = not multi
        if single_line_multi:
            detected_version_strings = (
                single_line_pattern.search(content)
                .group(0)
                .split(":")[1]
                .strip()
                .split(",")
            )
            return set(v.strip() for v in detected_version_strings), single_line_multi

    # Handle multi-line detection for specific products
    detected_version_strings = []
    if product == Product.WOW_CLASSIC:
        # Check for Current Classic directive
        current_classic_pattern = re.compile(
            InterfaceDirective.get_directive_pattern(
                InterfaceDirective.CURRENT_CLASSIC
            ),
            flags=re.MULTILINE,
        )
        classic_pattern = re.compile(
            InterfaceDirective.get_directive_pattern(InterfaceDirective.CLASSIC),
            flags=re.MULTILINE,
        )

        if current_classic_pattern.search(content):
            detected_version_strings.extend(
                current_classic_pattern.search(content)
                .group(0)
                .split(":")[1]
                .strip()
                .split(",")
            )
        if classic_pattern.search(content):
            detected_version_strings.extend(
                classic_pattern.search(content)
                .group(0)
                .split(":")[1]
                .strip()
                .split(",")
            )
    elif product == Product.WOW_CLASSIC_ERA:
        vanilla_pattern = re.compile(
            InterfaceDirective.get_directive_pattern(InterfaceDirective.VANILLA),
            flags=re.MULTILINE,
        )
        if vanilla_pattern.search(content):
            detected_version_strings.extend(
                vanilla_pattern.search(content)
                .group(0)
                .split(":")[1]
                .strip()
                .split(",")
            )

    return (
        set(v.strip() for v in detected_version_strings if v.strip()),
        single_line_multi,
    )


def get_versions_from_detected(
    detected_versions: Set[str], beta: bool, test: bool, version_cache: VersionCache
) -> Set[str]:
    """Convert detected version strings to actual versions with beta/test support."""
    from .version_client import product_version  # Import here to avoid circular imports

    versions: Set[str] = set()

    for d_version in detected_versions:
        if d_version.strip() not in versions:
            major = int(d_version.strip()[:-4])

            if major == 1:
                n_version = product_version(Product.WOW_CLASSIC_ERA, version_cache)
                versions.add(n_version)
                if test:
                    classic_era_ptr_version = product_version(
                        Product.WOW_CLASSIC_ERA_PTR, version_cache
                    )
                    if int(d_version) < int(classic_era_ptr_version) > int(n_version):
                        versions.add(classic_era_ptr_version)
            elif major < 11:
                n_version = product_version(Product.WOW_CLASSIC, version_cache)
                versions.add(n_version)
                if beta:
                    classic_beta_version = product_version(
                        Product.WOW_CLASSIC_BETA, version_cache
                    )
                    if int(d_version) < int(classic_beta_version) > int(n_version):
                        versions.add(classic_beta_version)
                if test:
                    classic_ptr_version = product_version(
                        Product.WOW_CLASSIC_PTR, version_cache
                    )
                    if int(d_version) < int(classic_ptr_version) > int(n_version):
                        versions.add(classic_ptr_version)
            else:
                n_version = product_version(Product.WOW, version_cache)
                versions.add(n_version)
                if beta:
                    beta_version = product_version(Product.WOW_BETA, version_cache)
                    if int(d_version) < int(beta_version) > int(n_version):
                        versions.add(beta_version)
                if test:
                    ptr_version = product_version(Product.WOW_TEST, version_cache)
                    if int(d_version) < int(ptr_version) > int(n_version):
                        versions.add(ptr_version)
                    ptr_version = product_version(Product.WOW_XPTR, version_cache)
                    if int(d_version) < int(ptr_version) > int(n_version):
                        versions.add(ptr_version)

    return versions


def collect_all_versions(
    product: Product, beta: bool, test: bool, version_cache: VersionCache
) -> Set[str]:
    """Collect all versions (base, beta, test) for a product."""
    from .version_client import product_version  # Import here to avoid circular imports

    base_version = product_version(product, version_cache)
    versions: Set[str] = {base_version}

    # Handle beta versions
    if beta:
        for beta_product in get_beta_products(product):
            beta_version = product_version(beta_product, version_cache)
            if int(beta_version) > int(base_version):
                versions.add(beta_version)

    # Handle test versions
    if test:
        for test_product in get_test_products(product):
            test_version = product_version(test_product, version_cache)
            if int(test_version) > int(base_version):
                versions.add(test_version)

    return versions
