"""
Test the functions that load libgmt.
"""
import ctypes
import shutil
import subprocess
import sys
import types
from pathlib import PurePath

import pytest
from pygmt.clib.loading import check_libgmt, clib_full_names, clib_names, load_libgmt
from pygmt.exceptions import GMTCLibError, GMTCLibNotFoundError, GMTOSError


class FakedLibGMT:  # pylint: disable=too-few-public-methods
    """
    Class for faking a GMT library.
    """

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return self._name


def test_check_libgmt():
    """
    Make sure check_libgmt fails when given a bogus library.
    """
    libgmt = FakedLibGMT("/path/to/libgmt.so")
    msg = (
        # pylint: disable=protected-access
        f"Error loading '{libgmt._name}'. "
        "Couldn't access function GMT_Create_Session. "
        "Ensure that you have installed an up-to-date GMT version 6 library. "
        "Please set the environment variable 'GMT_LIBRARY_PATH' to the "
        "directory of the GMT 6 library."
    )
    with pytest.raises(GMTCLibError, match=msg):
        check_libgmt(libgmt)


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


###############################################################################
# Tests for load_libgmt
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


def test_load_libgmt_with_broken_libraries(monkeypatch):
    """
    Test load_libgmt still works when a broken library is found.
    """
    # load the GMT library before mocking the ctypes.CDLL function
    loaded_libgmt = load_libgmt()

    def mock_ctypes_cdll_return(libname):
        """
        Mock the return value of ctypes.CDLL.

        Parameters
        ----------
        libname : str or FakedLibGMT or ctypes.CDLL
            Path to the GMT library, a faked GMT library or a working library
            loaded as ctypes.CDLL.

        Return
        ------
        object
            Either the loaded GMT library or the faked GMT library.
        """
        if isinstance(libname, FakedLibGMT):
            # libname is a faked GMT library, return the faked library
            return libname
        if isinstance(libname, str):
            # libname is an invalid library path in str type,
            # raise OSError like the original ctypes.CDLL
            raise OSError(f"Unable to find '{libname}'")
        # libname is a loaded GMT library
        return loaded_libgmt

    with monkeypatch.context() as mpatch:
        # pylint: disable=protected-access
        # mock the ctypes.CDLL using mock_ctypes_cdll_return()
        mpatch.setattr(ctypes, "CDLL", mock_ctypes_cdll_return)

        faked_libgmt1 = FakedLibGMT("/path/to/faked/libgmt1.so")
        faked_libgmt2 = FakedLibGMT("/path/to/faked/libgmt2.so")

        # case 1: two broken libraries
        # Raise the GMTCLibNotFoundError exception
        # The error message should contains information of both libraries
        lib_fullnames = [faked_libgmt1, faked_libgmt2]
        msg_regex = (
            fr"Error loading GMT shared library at '{faked_libgmt1._name}'.\n"
            fr"Error loading '{faked_libgmt1._name}'. Couldn't access.*\n"
            fr"Error loading GMT shared library at '{faked_libgmt2._name}'.\n"
            fr"Error loading '{faked_libgmt2._name}'. Couldn't access.*"
        )
        with pytest.raises(GMTCLibNotFoundError, match=msg_regex):
            load_libgmt(lib_fullnames=lib_fullnames)

        # case 2: broken library + invalid path
        lib_fullnames = [faked_libgmt1, "/invalid/path/to/libgmt.so"]
        msg_regex = (
            fr"Error loading GMT shared library at '{faked_libgmt1._name}'.\n"
            fr"Error loading '{faked_libgmt1._name}'. Couldn't access.*\n"
            "Error loading GMT shared library at '/invalid/path/to/libgmt.so'.\n"
            "Unable to find '/invalid/path/to/libgmt.so'"
        )
        with pytest.raises(GMTCLibNotFoundError, match=msg_regex):
            load_libgmt(lib_fullnames=lib_fullnames)

        # case 3: broken library + invalid path + working library
        lib_fullnames = [faked_libgmt1, "/invalid/path/to/libgmt.so", loaded_libgmt]
        assert check_libgmt(load_libgmt(lib_fullnames=lib_fullnames)) is None

        # case 4: invalid path + broken library + working library
        lib_fullnames = ["/invalid/path/to/libgmt.so", faked_libgmt1, loaded_libgmt]
        assert check_libgmt(load_libgmt(lib_fullnames=lib_fullnames)) is None

        # case 5: working library + broken library + invalid path
        lib_fullnames = [loaded_libgmt, faked_libgmt1, "/invalid/path/to/libgmt.so"]
        assert check_libgmt(load_libgmt(lib_fullnames=lib_fullnames)) is None

        # case 6: repeated broken library + working library
        lib_fullnames = [faked_libgmt1, faked_libgmt1, loaded_libgmt]
        assert check_libgmt(load_libgmt(lib_fullnames=lib_fullnames)) is None


###############################################################################
# Tests for clib_full_names
@pytest.fixture(scope="module", name="gmt_lib_names")
def fixture_gmt_lib_names():
    """
    Return a list of the library names for the current operating system.
    """
    return clib_names(sys.platform)


@pytest.fixture(scope="module", name="gmt_bin_dir")
def fixture_gmt_bin_dir():
    """
    Return GMT's bin directory.
    """
    return str(PurePath(shutil.which("gmt")).parent)


@pytest.fixture(scope="module", name="gmt_lib_realpath")
def fixture_gmt_lib_realpath():
    """
    Return the real path of the GMT library.
    """
    lib_realpath = subprocess.check_output(
        ["gmt", "--show-library"], encoding="utf-8"
    ).rstrip("\n")
    # On Windows, clib_full_names() returns paths with separator "\\",
    # but "gmt --show-library" returns paths with separator "/".
    # Use `str(PurePath(realpath)` to mimic the behavior of clib_full_names()
    return str(PurePath(lib_realpath))


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
        mpatch.setenv("GMT_LIBRARY_PATH", str(PurePath(gmt_lib_realpath).parent))
        mpatch.setenv("PATH", "")
        lib_fullpaths = clib_full_names()

        assert isinstance(lib_fullpaths, types.GeneratorType)
        assert list(lib_fullpaths) == [gmt_lib_realpath] + gmt_lib_names


def test_clib_full_names_gmt_library_path_undefined_path_included(
    monkeypatch, gmt_lib_names, gmt_lib_realpath, gmt_bin_dir
):
    """
    Make sure that clib_full_names() returns a generator with expected names
    when GMT_LIBRARY_PATH is undefined and PATH includes GMT's bin path.
    """
    with monkeypatch.context() as mpatch:
        mpatch.delenv("GMT_LIBRARY_PATH", raising=False)
        mpatch.setenv("PATH", gmt_bin_dir)
        lib_fullpaths = clib_full_names()

        assert isinstance(lib_fullpaths, types.GeneratorType)
        # Windows: find_library() searches the library in PATH, so one more
        npath = 2 if sys.platform == "win32" else 1
        assert list(lib_fullpaths) == [gmt_lib_realpath] * npath + gmt_lib_names


def test_clib_full_names_gmt_library_path_defined_path_included(
    monkeypatch, gmt_lib_names, gmt_lib_realpath, gmt_bin_dir
):
    """
    Make sure that clib_full_names() returns a generator with expected names
    when GMT_LIBRARY_PATH is defined and PATH includes GMT's bin path.
    """
    with monkeypatch.context() as mpatch:
        mpatch.setenv("GMT_LIBRARY_PATH", str(PurePath(gmt_lib_realpath).parent))
        mpatch.setenv("PATH", gmt_bin_dir)
        lib_fullpaths = clib_full_names()

        assert isinstance(lib_fullpaths, types.GeneratorType)
        # Windows: find_library() searches the library in PATH, so one more
        npath = 3 if sys.platform == "win32" else 2
        assert list(lib_fullpaths) == [gmt_lib_realpath] * npath + gmt_lib_names


def test_clib_full_names_gmt_library_path_incorrect_path_included(
    monkeypatch, gmt_lib_names, gmt_lib_realpath, gmt_bin_dir
):
    """
    Make sure that clib_full_names() returns a generator with expected names
    when GMT_LIBRARY_PATH is defined but incorrect and PATH includes GMT's bin
    path.
    """
    with monkeypatch.context() as mpatch:
        mpatch.setenv("GMT_LIBRARY_PATH", "/not/a/valid/library/path")
        mpatch.setenv("PATH", gmt_bin_dir)
        lib_fullpaths = clib_full_names()

        assert isinstance(lib_fullpaths, types.GeneratorType)
        # Windows: find_library() searches the library in PATH, so one more
        npath = 2 if sys.platform == "win32" else 1
        assert list(lib_fullpaths) == [gmt_lib_realpath] * npath + gmt_lib_names
