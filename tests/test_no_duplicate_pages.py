import os


def test_no_duplicate_page_basenames():
    roots = ["ui/pages"]
    names = {}

    for base in roots:
        for dp, _, files in os.walk(base):
            for filename in files:
                if filename.endswith(".py"):
                    assert (
                        filename not in names
                    ), f"Duplicate page filename: {filename} in {dp} and {names[filename]}"
                    names[filename] = dp
