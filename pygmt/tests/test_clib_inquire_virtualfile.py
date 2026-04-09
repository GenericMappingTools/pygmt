"""
Test the Session.inquire_virtualfile method.
"""

from pygmt import clib


def test_inquire_virtualfile():
    """
    Test that the inquire_virtualfile method returns the correct family.

    Currently, only output virtual files are tested.
    """
    with clib.Session() as lib:
        for family in [
            "GMT_IS_DATASET",
            "GMT_IS_DATASET|GMT_VIA_MATRIX",
            "GMT_IS_DATASET|GMT_VIA_VECTOR",
        ]:
            with lib.open_virtualfile(
                family, "GMT_IS_PLP", "GMT_OUT|GMT_IS_REFERENCE", None
            ) as vfile:
                assert lib.inquire_virtualfile(vfile) == lib["GMT_IS_DATASET"]

        for family, geometry in [
            ("GMT_IS_GRID", "GMT_IS_SURFACE"),
            ("GMT_IS_IMAGE", "GMT_IS_SURFACE"),
            ("GMT_IS_CUBE", "GMT_IS_VOLUME"),
            ("GMT_IS_PALETTE", "GMT_IS_NONE"),
            ("GMT_IS_POSTSCRIPT", "GMT_IS_NONE"),
        ]:
            with lib.open_virtualfile(family, geometry, "GMT_OUT", None) as vfile:
                assert lib.inquire_virtualfile(vfile) == lib[family]
