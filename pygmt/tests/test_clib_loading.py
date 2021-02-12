"""
Test the functions that load libgmt.
"""
import os
import shutil
import subprocess
import sys
import types

import pytest
from pygmt.clib.loading import check_libgmt, clib_full_names, clib_names, load_libgmt
from pygmt.exceptions import GMTCLibError, GMTCLibNotFoundError, GMTOSError


def test_check_libgmt():
    """
    Make sure check_libgmt fails when given a bogus library.
    """
    with pytest.raises(GMTCLibError):
        check_libgmt(dict())


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


def test_clib_full_names(monkeypatch):
    """
    Make sure that clib_full_names() returns a generator with expected length
    for different cases.
    """

    def check_clib_list_length(os_name, lib_fullpaths, linux=1, macos=1, windows=1):
        """
        A utitlity function to check the length of lib_fullpaths in different
        OS.
        """
        length = len(list(lib_fullpaths))
        if os_name.startswith("linux"):
            assert length == linux
        elif os_name == "darwin":
            assert length == macos
        elif os_name == "win32":
            assert length == windows

    os_name = sys.platform
    # 1. GMT_LIBRARY_PATH and PATH are undefined
    with monkeypatch.context() as mpatch:
        mpatch.delenv("GMT_LIBRARY_PATH", raising=False)
        mpatch.setenv("PATH", "")

        lib_fullpaths = clib_full_names()
        assert isinstance(lib_fullpaths, types.GeneratorType)

        lib_fullpaths = list(lib_fullpaths)
        if os_name.startswith("linux"):
            assert lib_fullpaths == ["libgmt.so"]
        elif os_name == "darwin":
            assert lib_fullpaths == ["libgmt.dylib"]
        elif os_name == "win32":
            assert lib_fullpaths == ["gmt.dll", "gmt_w64.dll", "gmt_w32.dll"]

    bin_realpath = shutil.which("gmt")
    lib_realpath = subprocess.check_output(
        [bin_realpath, "--show-library"], encoding="utf-8"
    ).rstrip("\n")

    # 2. GMT_LIBRARY_PATH is defined but PATH is undefined
    with monkeypatch.context() as mpatch:
        mpatch.setenv("GMT_LIBRARY_PATH", os.path.dirname(lib_realpath))
        mpatch.setenv("PATH", "")

        lib_fullpaths = clib_full_names()
        assert isinstance(lib_fullpaths, types.GeneratorType)

        lib_fullpaths = list(lib_fullpaths)
        if os_name.startswith("linux"):
            assert lib_fullpaths == [lib_realpath, "libgmt.so"]
        elif os_name == "darwin":
            assert lib_fullpaths == [lib_realpath, "libgmt.dylib"]
        elif os_name == "win32":
            assert lib_fullpaths == [
                lib_realpath,
                "gmt.dll",
                "gmt_w64.dll",
                "gmt_w32.dll",
            ]

    # 3. GMT_LIBRARY_PATH is undefined but PATH is defined
    with monkeypatch.context() as mpatch:
        mpatch.delenv("GMT_LIBRARY_PATH", raising=False)
        mpatch.setenv("PATH", os.path.dirname(bin_realpath))

        lib_fullpaths = clib_full_names()
        assert isinstance(lib_fullpaths, types.GeneratorType)

        lib_fullpaths = list(lib_fullpaths)
        if os_name.startswith("linux"):
            assert lib_fullpaths == [lib_realpath, "libgmt.so"]
        elif os_name == "darwin":
            assert lib_fullpaths == [lib_realpath, "libgmt.dylib"]
        elif os_name == "win32":
            assert lib_fullpaths == [
                lib_realpath,
                lib_realpath,
                "gmt.dll",
                "gmt_w64.dll",
                "gmt_w32.dll",
            ]

    # 4. both GMT_LIBRARY_PATH and PATH are defined
    with monkeypatch.context() as mpatch:
        mpatch.setenv("GMT_LIBRARY_PATH", os.path.dirname(lib_realpath))
        mpatch.setenv("PATH", os.path.dirname(bin_realpath))

        lib_fullpaths = clib_full_names()
        assert isinstance(lib_fullpaths, types.GeneratorType)

        lib_fullpaths = list(lib_fullpaths)
        if os_name.startswith("linux"):
            assert lib_fullpaths == [lib_realpath, lib_realpath, "libgmt.so"]
        elif os_name == "darwin":
            assert lib_fullpaths == [lib_realpath, lib_realpath, "libgmt.dylib"]
        elif os_name == "win32":
            assert lib_fullpaths == [
                lib_realpath,
                lib_realpath,
                lib_realpath,
                "gmt.dll",
                "gmt_w64.dll",
                "gmt_w32.dll",
            ]
