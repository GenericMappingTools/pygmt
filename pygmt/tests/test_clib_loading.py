"""
Test the functions that load libgmt
"""
import pytest

from ..clib.loading import clib_name, load_libgmt, check_libgmt
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
    env = {"GMT_LIBRARY_PATH": "not/a/real/path"}
    with pytest.raises(GMTCLibNotFoundError):
        load_libgmt(env=env)


def test_clib_name():
    "Make sure we get the correct library name for different OS names"
    for linux in ["linux", "linux2", "linux3"]:
        assert clib_name(linux) == ["libgmt.so"]
    assert clib_name("darwin") == ["libgmt.dylib"]
    assert clib_name("win32") == ["gmt.dll", "gmt_w64.dll", "gmt_w32.dll"]
    with pytest.raises(GMTOSError):
        clib_name("meh")
