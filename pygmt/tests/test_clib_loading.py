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


@pytest.fixture(scope="module", name="os_name")
def fixture_os_name():
    """
    Return the name of the current operating system.
    """
    return sys.platform


@pytest.fixture(scope="module", name="gmt_lib_names")
def fixture_gmt_lib_names(os_name):
    """
    Return a list of the library names for the current operating system.
    """
    return clib_names(os_name)


@pytest.fixture(scope="module", name="gmt_bin_realpath")
def fixture_gmt_bin_realpath():
    """
    Return the real path of GMT's "gmt" command.
    """
    return shutil.which("gmt")


@pytest.fixture(scope="module", name="gmt_lib_realpath")
def fixture_gmt_lib_realpath():
    """
    Return the real path of the GMT library.
    """
    return subprocess.check_output(["gmt", "--show-library"], encoding="utf-8").rstrip(
        "\n"
    )


def test_clib_full_names_gmt_library_path_undefined_path_empty(
    monkeypatch, gmt_lib_names
):
    """
    Make sure that clib_full_names() returns a generator with expected names
    when GMT_LIBRARY_PATH is undefined and PATH is empty.
    """
    with monkeypatch.context() as mpatch:
        mpatch.delenv("GMT_LIBRARY_PATH", raising=False)
        mpatch.setenv("PATH", "")

        lib_fullpaths = clib_full_names()
        assert isinstance(lib_fullpaths, types.GeneratorType)
        assert list(lib_fullpaths) == gmt_lib_names


def test_clib_full_names_gmt_library_path_defined_path_empty(
    monkeypatch, gmt_lib_names, gmt_lib_realpath
):
    """
    Make sure that clib_full_names() returns a generator with expected names
    when GMT_LIBRARY_PATH is defined and PATH is empty.
    """
    with monkeypatch.context() as mpatch:
        mpatch.setenv("GMT_LIBRARY_PATH", os.path.dirname(gmt_lib_realpath))
        mpatch.setenv("PATH", "")

        lib_fullpaths = clib_full_names()
        assert isinstance(lib_fullpaths, types.GeneratorType)
        assert list(lib_fullpaths) == [gmt_lib_realpath] + gmt_lib_names


def test_clib_full_names_gmt_library_path_undefined_path_included(
    monkeypatch, gmt_lib_names, gmt_lib_realpath, gmt_bin_realpath, os_name
):
    """
    Make sure that clib_full_names() returns a generator with expected names
    when GMT_LIBRARY_PATH is undefined and PATH includes GMT's bin path.
    """
    with monkeypatch.context() as mpatch:
        mpatch.delenv("GMT_LIBRARY_PATH", raising=False)
        mpatch.setenv("PATH", os.path.dirname(gmt_bin_realpath))

        lib_fullpaths = clib_full_names()
        assert isinstance(lib_fullpaths, types.GeneratorType)

        lib_fullpaths = list(lib_fullpaths)
        if os_name.startswith("linux") or os_name == "darwin":
            assert lib_fullpaths == [gmt_lib_realpath] + gmt_lib_names
        elif os_name == "win32":
            # On Windows: we also call find_library() to find the library in PATH
            assert lib_fullpaths == [gmt_lib_realpath] * 2 + gmt_lib_names


def test_clib_full_names_gmt_library_path_defined_path_included(
    monkeypatch, gmt_lib_names, gmt_lib_realpath, gmt_bin_realpath, os_name
):
    """
    Make sure that clib_full_names() returns a generator with expected names
    when GMT_LIBRARY_PATH is defined and PATH includes GMT's bin path.
    """
    with monkeypatch.context() as mpatch:
        mpatch.setenv("GMT_LIBRARY_PATH", os.path.dirname(gmt_lib_realpath))
        mpatch.setenv("PATH", os.path.dirname(gmt_bin_realpath))

        lib_fullpaths = clib_full_names()
        assert isinstance(lib_fullpaths, types.GeneratorType)

        lib_fullpaths = list(lib_fullpaths)
        if os_name.startswith("linux") or os_name == "darwin":
            assert lib_fullpaths == [gmt_lib_realpath] * 2 + gmt_lib_names
        elif os_name == "win32":
            assert lib_fullpaths == [gmt_lib_realpath] * 3 + gmt_lib_names


def test_clib_full_names_gmt_library_path_incorrect_path_included(
    monkeypatch, gmt_lib_names, gmt_lib_realpath, gmt_bin_realpath, os_name
):
    """
    Make sure that clib_full_names() returns a generator with expected names
    when GMT_LIBRARY_PATH is defined but incorrect and PATH includes GMT's bin path.
    """
    with monkeypatch.context() as mpatch:
        mpatch.setenv("GMT_LIBRARY_PATH", "/not/a/valid/library/path")
        mpatch.setenv("PATH", os.path.dirname(gmt_bin_realpath))

        lib_fullpaths = clib_full_names()
        assert isinstance(lib_fullpaths, types.GeneratorType)

        lib_fullpaths = list(lib_fullpaths)
        if os_name.startswith("linux") or os_name == "darwin":
            assert lib_fullpaths == [gmt_lib_realpath] + gmt_lib_names
        elif os_name == "win32":
            assert lib_fullpaths == [gmt_lib_realpath] * 2 + gmt_lib_names
