"""
Test the Session.write_data method.
"""

import pytest
from pygmt import clib
from pygmt.exceptions import GMTCLibError
from pygmt.tests.test_clib import mock


def test_write_data_fails():
    """
    Check that write data raises an exception for non-zero return codes.
    """
    # It's hard to make the C API function fail without causing a Segmentation
    # Fault. Can't test this if by giving a bad file name because if
    # output=='', GMT will just write to stdout and spaces are valid file
    # names. Use a mock instead just to exercise this part of the code.
    with clib.Session() as lib:
        with mock(lib, "GMT_Write_Data", returns=1):
            with pytest.raises(GMTCLibError):
                lib.write_data(
                    "GMT_IS_VECTOR",
                    "GMT_IS_POINT",
                    "GMT_WRITE_SET",
                    [1] * 6,
                    "some-file-name",
                    None,
                )
