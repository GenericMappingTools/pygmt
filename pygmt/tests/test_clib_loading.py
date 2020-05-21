"""
Test the functions that load libgmt
"""
import os
import pytest

from ..clib.loading import clib_names, load_libgmt, check_libgmt
from ..exceptions import GMTCLibError, GMTOSError, GMTCLibNotFoundError


def test_check_libgmt():
    "Make sure check_libgmt fails when given a bogus library"
    with pytest.raises(GMTCLibError):
        check_libgmt(dict())


def test_load_libgmt():
    "Test that loading libgmt works and doesn't crash."
    check_libgmt(load_libgmt())


def test_load_libgmt_fail():
    "Test that loading fails when given a bad library path."
    # save the old value (if any) before setting a fake "GMT_LIBRARY_PATH"
    old_gmt_library_path = os.environ.get("GMT_LIBRARY_PATH")

    os.environ["GMT_LIBRARY_PATH"] = "/not/a/real/path"
    with pytest.raises(GMTCLibNotFoundError):
        load_libgmt()

    # revert back to the original status (if any)
    if old_gmt_library_path:
        os.environ["GMT_LIBRARY_PATH"] = old_gmt_library_path
    else:
        del os.environ["GMT_LIBRARY_PATH"]


def test_clib_names():
    "Make sure we get the correct library name for different OS names"
    for linux in ["linux", "linux2", "linux3"]:
        assert clib_names(linux) == ["libgmt.so"]
    assert clib_names("darwin") == ["libgmt.dylib"]
    assert clib_names("win32") == ["gmt.dll", "gmt_w64.dll", "gmt_w32.dll"]
    with pytest.raises(GMTOSError):
        clib_names("meh")
