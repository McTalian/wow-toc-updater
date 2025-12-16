import difflib

from toc_interface_updater.constants import InterfaceDirective, TocSuffix
from toc_interface_updater.toc_types import Product
from toc_interface_updater.update import main


def test_update_toc_files(toc_files, product_versions, monkeypatch):
    # Change the working directory to the temporary directory with the .toc files
    monkeypatch.chdir(toc_files)

    # Simulate running the script without any flags
    monkeypatch.setattr("sys.argv", ["update.py"])

    # Run the update script
    main()

    # Check the contents of the updated files
    expected_content = {
        "default.toc": f"{InterfaceDirective.BASE} {product_versions[Product.WOW]}\n\nfile.lua\n",
        f"specific-{TocSuffix.CLASSIC}.toc": f"{InterfaceDirective.BASE} {product_versions[Product.WOW_CLASSIC]}\n\nfile.lua\n",
        "multi.toc": f"{InterfaceDirective.BASE} {product_versions[Product.WOW]}\n{InterfaceDirective.VANILLA} {product_versions[Product.WOW_CLASSIC_ERA]}\n{InterfaceDirective.CLASSIC} {product_versions[Product.WOW_CLASSIC]}\n{InterfaceDirective.CURRENT_CLASSIC} {product_versions[Product.WOW_CLASSIC]}\n\nfile.lua\n",
        "multi-oneline.toc": f"{InterfaceDirective.BASE} {product_versions[Product.WOW_CLASSIC_ERA]}, {product_versions[Product.WOW_CLASSIC]}, {product_versions[Product.WOW]}\n\nfile.lua\n",
        f"specific-{TocSuffix.MAINLINE}.toc": f"{InterfaceDirective.BASE} {product_versions[Product.WOW]}\n\nfile.lua\n",
        f"specific_{TocSuffix.CURRENT_CLASSIC}.toc": f"{InterfaceDirective.BASE} {product_versions[Product.WOW_CLASSIC]}\n\nfile.lua\n",
    }

    for filename, expected in expected_content.items():
        file_path = toc_files / filename
        actual = file_path.read_text()
        if actual != expected:
            diff = "\n".join(
                difflib.unified_diff(
                    expected.splitlines(),
                    actual.splitlines(),
                    fromfile="expected",
                    tofile="actual",
                    lineterm="",
                )
            )
            print(f"\nDifference in {filename}:\n{diff}")
        assert actual == expected, f"File: {filename}"


def test_update_toc_files_with_ptr_flag(toc_files, product_versions, monkeypatch):
    # Change the working directory to the temporary directory with the .toc files
    monkeypatch.chdir(toc_files)

    # Simulate the PTR flag
    monkeypatch.setattr("sys.argv", ["update.py", "--ptr"])

    base_retail_version = product_versions[Product.WOW]
    retail_ptr_versions = set()
    retail_ptr_versions.add(base_retail_version)
    retail_ptr_check = product_versions[Product.WOW_TEST]
    if int(retail_ptr_check) > int(base_retail_version):
        retail_ptr_versions.add(retail_ptr_check)
    retail_ptr_check = product_versions[Product.WOW_XPTR]
    if int(retail_ptr_check) > int(base_retail_version):
        retail_ptr_versions.add(retail_ptr_check)
    retail_ptr_versions = ", ".join(sorted(retail_ptr_versions, key=lambda x: int(x)))

    base_classic_version = product_versions[Product.WOW_CLASSIC]
    classic_ptr_versions = set()
    classic_ptr_versions.add(base_classic_version)
    classic_ptr_check = product_versions[Product.WOW_CLASSIC_PTR]
    if int(classic_ptr_check) > int(base_classic_version):
        classic_ptr_versions.add(classic_ptr_check)
    classic_ptr_versions = ", ".join(sorted(classic_ptr_versions, key=lambda x: int(x)))

    base_classic_era_version = product_versions[Product.WOW_CLASSIC_ERA]
    classic_era_ptr_versions = set()
    classic_era_ptr_versions.add(base_classic_era_version)
    classic_era_ptr_check = product_versions[Product.WOW_CLASSIC_ERA_PTR]
    if int(classic_era_ptr_check) > int(base_classic_era_version):
        classic_era_ptr_versions.add(classic_era_ptr_check)
    classic_era_ptr_versions = ", ".join(
        sorted(classic_era_ptr_versions, key=lambda x: int(x))
    )

    # Run the update script
    main()

    # Check the contents of the updated files
    expected_content = {
        "default.toc": f"{InterfaceDirective.BASE} {retail_ptr_versions}\n\nfile.lua\n",
        f"specific-{TocSuffix.CLASSIC}.toc": f"{InterfaceDirective.BASE} {classic_ptr_versions}\n\nfile.lua\n",
        "multi.toc": f"{InterfaceDirective.BASE} {retail_ptr_versions}\n{InterfaceDirective.VANILLA} {classic_era_ptr_versions}\n{InterfaceDirective.CLASSIC} {classic_ptr_versions}\n{InterfaceDirective.CURRENT_CLASSIC} {classic_ptr_versions}\n\nfile.lua\n",
        "multi-oneline.toc": f"{InterfaceDirective.BASE} {classic_era_ptr_versions}, {classic_ptr_versions}, {retail_ptr_versions}\n\nfile.lua\n",
        f"specific-{TocSuffix.MAINLINE}.toc": f"{InterfaceDirective.BASE} {retail_ptr_versions}\n\nfile.lua\n",
        f"specific_{TocSuffix.CURRENT_CLASSIC}.toc": f"{InterfaceDirective.BASE} {classic_ptr_versions}\n\nfile.lua\n",
    }

    for filename, expected in expected_content.items():
        file_path = toc_files / filename
        actual = file_path.read_text()
        if actual != expected:
            diff = "\n".join(
                difflib.unified_diff(
                    expected.splitlines(),
                    actual.splitlines(),
                    fromfile="expected",
                    tofile="actual",
                    lineterm="",
                )
            )
            print(f"\nDifference in {filename}:\n{diff}")
        assert actual == expected, f"File: {filename}"


def test_update_toc_files_with_beta_flag(toc_files, product_versions, monkeypatch):
    # Change the working directory to the temporary directory with the .toc files
    monkeypatch.chdir(toc_files)

    # Simulate the Beta flag
    monkeypatch.setattr("sys.argv", ["update.py", "--beta"])

    retail_beta_versions = set()
    base_retail_version = product_versions[Product.WOW]
    retail_beta_versions.add(base_retail_version)
    retail_beta_check = product_versions[Product.WOW_BETA]
    if int(retail_beta_check) > int(base_retail_version):
        retail_beta_versions.add(retail_beta_check)
    retail_beta_versions = ", ".join(sorted(retail_beta_versions, key=lambda x: int(x)))

    classic_beta_versions = set()
    base_classic_version = product_versions[Product.WOW_CLASSIC]
    classic_beta_versions.add(base_classic_version)
    classic_beta_check = product_versions[Product.WOW_CLASSIC_BETA]
    if int(classic_beta_check) > int(base_classic_version):
        classic_beta_versions.add(classic_beta_check)
    classic_beta_versions = ", ".join(
        sorted(classic_beta_versions, key=lambda x: int(x))
    )

    classic_era_beta_versions = set()
    base_classic_era_version = product_versions[Product.WOW_CLASSIC_ERA]
    classic_era_beta_versions.add(base_classic_era_version)
    # The classic era beta product does not return any version information
    # classic_era_beta_check = product_versions['wow_classic_era_beta']
    # if int(classic_era_beta_check) > int(base_classic_era_version):
    #     classic_era_beta_versions.add(classic_era_beta_check)
    classic_era_beta_versions = ", ".join(
        sorted(classic_era_beta_versions, key=lambda x: int(x))
    )

    # Run the update script
    main()

    # Check the contents of the updated files
    expected_content = {
        "default.toc": f"{InterfaceDirective.BASE} {retail_beta_versions}\n\nfile.lua\n",
        f"specific-{TocSuffix.CLASSIC}.toc": f"{InterfaceDirective.BASE} {classic_beta_versions}\n\nfile.lua\n",
        "multi.toc": f"{InterfaceDirective.BASE} {retail_beta_versions}\n{InterfaceDirective.VANILLA} {classic_era_beta_versions}\n{InterfaceDirective.CLASSIC} {classic_beta_versions}\n{InterfaceDirective.CURRENT_CLASSIC} {classic_beta_versions}\n\nfile.lua\n",
        "multi-oneline.toc": f"{InterfaceDirective.BASE} {classic_era_beta_versions}, {classic_beta_versions}, {retail_beta_versions}\n\nfile.lua\n",
        f"specific-{TocSuffix.MAINLINE}.toc": f"{InterfaceDirective.BASE} {retail_beta_versions}\n\nfile.lua\n",
        f"specific_{TocSuffix.CURRENT_CLASSIC}.toc": f"{InterfaceDirective.BASE} {classic_beta_versions}\n\nfile.lua\n",
    }

    for filename, expected in expected_content.items():
        file_path = toc_files / filename
        actual = file_path.read_text()
        if actual != expected:
            diff = "\n".join(
                difflib.unified_diff(
                    expected.splitlines(),
                    actual.splitlines(),
                    fromfile="expected",
                    tofile="actual",
                    lineterm="",
                )
            )
            print(f"\nDifference in {filename}:\n{diff}")
        assert actual == expected, f"File: {filename}"
