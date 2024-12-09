"""
Test the read function.
"""

import pytest
from pygmt import read


def test_read_invalid_kind():
    """
    Test that an invalid kind raises a ValueError.
    """
    with pytest.raises(ValueError, match="Invalid kind"):
        read("file.cpt", kind="cpt")


def test_read_invalid_arguments():
    """
    Test that invalid arguments raise a ValueError for non-'dataset' kind.
    """
    with pytest.raises(ValueError, match="Only the 'dataset' kind supports"):
        read("file.nc", kind="grid", column_names="foo")

    with pytest.raises(ValueError, match="Only the 'dataset' kind supports"):
        read("file.nc", kind="grid", header=1)

    with pytest.raises(ValueError, match="Only the 'dataset' kind supports"):
        read("file.nc", kind="grid", dtype="float")
