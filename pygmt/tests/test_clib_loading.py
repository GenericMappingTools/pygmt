"""
Test the functions that load libgmt.
"""
import subprocess
import sys

import pytest
from pygmt.clib.loading import check_libgmt, clib_names, load_libgmt
from pygmt.exceptions import GMTCLibError, GMTCLibNotFoundError, GMTOSError


def test_check_libgmt():
    """
    Make sure check_libgmt fails when given a bogus library.
    """
    # create a fake library with a "_name" property
    def libgmt():
        pass

    libgmt._name = "/path/to/libgmt.so"  # pylint: disable=protected-access
    msg = (
        f"Error loading '{libgmt._name}'. "  # pylint: disable=protected-access
        "Couldn't access function GMT_Create_Session. "
        "Maybe loading an old version of the GMT shared library."
    )
    with pytest.raises(GMTCLibError, match=msg):
        check_libgmt(libgmt)


def test_load_libgmt():
    """
    Test that loading libgmt works and doesn't crash.
    """
    check_libgmt(load_libgmt())


@pytest.mark.skipif(sys.platform == "win32", reason="run on UNIX platforms only")
def test_load_libgmt_fails(monkeypatch):
    """
    Test that GMTCLibNotFoundError is raised when GMT's shared library cannot
    be found.
    """
    with monkeypatch.context() as mpatch:
        mpatch.setattr(sys, "platform", "win32")  # pretend to be on Windows
        mpatch.setattr(
            subprocess, "check_output", lambda cmd, encoding: "libfakegmt.so"
        )
        with pytest.raises(GMTCLibNotFoundError):
            check_libgmt(load_libgmt())


def test_load_libgmt_with_a_bad_library_path(monkeypatch):
    """
    Test that loading still works when given a bad library path.
    """
    # Set a fake "GMT_LIBRARY_PATH"
    monkeypatch.setenv("GMT_LIBRARY_PATH", "/not/a/real/path")
    assert check_libgmt(load_libgmt()) is None


def test_clib_names():
    """
    Make sure we get the correct library name for different OS names.
    """
    for linux in ["linux", "linux2", "linux3"]:
        assert clib_names(linux) == ["libgmt.so"]
    assert clib_names("darwin") == ["libgmt.dylib"]
    assert clib_names("win32") == ["gmt.dll", "gmt_w64.dll", "gmt_w32.dll"]
    for freebsd in ["freebsd10", "freebsd11", "freebsd12"]:
        assert clib_names(freebsd) == ["libgmt.so"]
    with pytest.raises(GMTOSError):
        clib_names("meh")
