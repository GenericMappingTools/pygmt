"""
Test the functions that load libgmt
"""
import os

import pytest

from ..clib.loading import clib_name, load_libgmt, check_libgmt, get_clib_path
from .. import clib
from ..exceptions import GMTCLibError, GMTOSError, GMTCLibNotFoundError


def test_load_libgmt():
    "Test that loading libgmt works and doesn't crash."
    load_libgmt()


def test_load_libgmt_fail():
    "Test that loading fails when given a bad library path."
    env = {"GMT_LIBRARY_PATH": "not/a/real/path"}
    with pytest.raises(GMTCLibNotFoundError):
        load_libgmt(env=env)


def test_get_clib_path():
    "Test that the correct path is found when setting GMT_LIBRARY_PATH."
    # Get the real path to the library first
    with clib.Session() as lib:
        libpath = lib.info["library path"]
    libdir = os.path.dirname(libpath)
    # Assign it to the environment variable but keep a backup value to restore
    # later
    env = {"GMT_LIBRARY_PATH": libdir}

    # Check that the path is determined correctly
    path_used = get_clib_path(env=env)
    assert os.path.samefile(path_used, libpath)
    assert os.path.dirname(path_used) == libdir

    # Check that loading libgmt works
    load_libgmt(env=env)


def test_check_libgmt():
    "Make sure check_libgmt fails when given a bogus library"
    with pytest.raises(GMTCLibError):
        check_libgmt(dict())


def test_clib_name():
    "Make sure we get the correct library name for different OS names"
    for linux in ["linux", "linux2", "linux3"]:
        assert clib_name(linux) == "libgmt.so"
    assert clib_name("darwin") == "libgmt.dylib"
    assert clib_name("win32", is_64bit=True) == "gmt_w64.dll"
    assert clib_name("win32", is_64bit=False) == "gmt_w32.dll"
    with pytest.raises(GMTOSError):
        clib_name("meh")
