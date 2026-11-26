def test_package_import_and_version() -> None:
    import movingspace

    assert movingspace.__version__ == "0.1.0.dev0"
