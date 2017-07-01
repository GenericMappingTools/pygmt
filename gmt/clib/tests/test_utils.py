"""
Test the utility functions.
"""
from .. import load_libgmt


def test_load_libgmt():
    "Test that loading libgmt works and doesn't crash."
    libgmt = load_libgmt()
    assert hasattr(libgmt, 'GMT_Create_Session')
