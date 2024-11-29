"""
Test the functions that load libgmt.
"""

import ctypes
import os
import shutil
import subprocess
import sys
import types
from pathlib import PurePath

import pytest
from pygmt.clib.loading import (
    check_libgmt,
    clib_full_names,
    clib_names,
    get_gmt_version,
    load_libgmt,
)
from pygmt.clib.session import Session
from pygmt.exceptions import GMTCLibError, GMTCLibNotFoundError, GMTOSError


class FakedLibGMT:
    """
    Class for faking a GMT library.
    """

    def __init__(self, name):
        self._name = name

    def __str__(self):
        """
        String representation of the object.
        """
        return self._name


def test_check_libgmt():
    """
    Make sure check_libgmt fails when given a bogus library.
    """
    libgmt = FakedLibGMT("/path/to/libgmt.so")
    msg = f"Error loading '{libgmt}'. Couldn't access function GMT_Create_Session."
    with pytest.raises(GMTCLibError, match=msg):
        check_libgmt(libgmt)


def test_clib_names():
    """
    Make sure we get the correct library name for different OS names.
    """
    assert clib_names("linux") == ["libgmt.so"]
    assert clib_names("darwin") == ["libgmt.dylib"]
    assert clib_names("win32") == ["gmt.dll", "gmt_w64.dll", "gmt_w32.dll"]
    for freebsd in ["freebsd10", "freebsd11", "freebsd12"]:
        assert clib_names(freebsd) == ["libgmt.so"]
    with pytest.raises(GMTOSError):
        clib_names("meh")


###############################################################################
# Test load_libgmt
@pytest.mark.benchmark
def test_load_libgmt():
    """
    Test that loading libgmt works and doesn't crash.
    """
    check_libgmt(load_libgmt())


def test_load_libgmt_fails(monkeypatch):
    """
    Test that GMTCLibNotFoundError is raised when GMT's shared library cannot be found.
    """
    with monkeypatch.context() as mpatch:
        if sys.platform == "win32":
            mpatch.setattr(ctypes.util, "find_library", lambda name: "fakegmt.dll")  # noqa: ARG005
        mpatch.setattr(
            sys,
            "platform",
            # Pretend to be on macOS if running on Linux, and vice versa
            "darwin" if sys.platform == "linux" else "linux",
        )
        mpatch.setattr(
            subprocess,
            "check_output",
            lambda cmd, encoding: "libfakegmt.so",  # noqa: ARG005
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


class TestLibgmtBrokenLibs:
    """
    Test that load_libgmt still works when a broken library is found.
    """

    # load the GMT library before mocking the ctypes.CDLL function
    loaded_libgmt = load_libgmt()
    invalid_path = "/invalid/path/to/libgmt.so"
    faked_libgmt1 = FakedLibGMT("/path/to/faked/libgmt1.so")
    faked_libgmt2 = FakedLibGMT("/path/to/faked/libgmt2.so")

    def _mock_ctypes_cdll_return(self, libname):
        """
        Mock the return value of ctypes.CDLL.

        Parameters
        ----------
        libname : str or FakedLibGMT or ctypes.CDLL
            Path to the GMT library, a faked GMT library, or a working library
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
            # libname is an invalid library path in string type,
            # raise OSError like the original ctypes.CDLL
            msg = f"Unable to find '{libname}'."
            raise OSError(msg)
        # libname is a loaded GMT library
        return self.loaded_libgmt

    @pytest.fixture
    def _mock_ctypes(self, monkeypatch):
        """
        Patch the ctypes.CDLL function.
        """
        monkeypatch.setattr(ctypes, "CDLL", self._mock_ctypes_cdll_return)

    @pytest.mark.usefixtures("_mock_ctypes")
    def test_two_broken_libraries(self):
        """
        Case 1: two broken libraries.

        Raise the GMTCLibNotFoundError exception. Error message should contain
        information of both libraries that failed to load properly.
        """
        lib_fullnames = [self.faked_libgmt1, self.faked_libgmt2]
        msg_regex = (
            rf"Error loading GMT shared library at '{self.faked_libgmt1._name}'.\n"
            rf"Error loading '{self.faked_libgmt1._name}'. Couldn't access.*\n"
            rf"Error loading GMT shared library at '{self.faked_libgmt2._name}'.\n"
            f"Error loading '{self.faked_libgmt2._name}'. Couldn't access.*"
        )
        with pytest.raises(GMTCLibNotFoundError, match=msg_regex):
            load_libgmt(lib_fullnames=lib_fullnames)

    @pytest.mark.usefixtures("_mock_ctypes")
    def test_load_brokenlib_invalidpath(self):
        """
        Case 2: broken library + invalid path.

        Raise the GMTCLibNotFoundError exception. Error message should contain
        information of one library that failed to load and one invalid path.
        """
        lib_fullnames = [self.faked_libgmt1, self.invalid_path]
        msg_regex = (
            rf"Error loading GMT shared library at '{self.faked_libgmt1._name}'.\n"
            rf"Error loading '{self.faked_libgmt1._name}'. Couldn't access.*\n"
            rf"Error loading GMT shared library at '{self.invalid_path}'.\n"
            f"Unable to find '{self.invalid_path}'"
        )
        with pytest.raises(GMTCLibNotFoundError, match=msg_regex):
            load_libgmt(lib_fullnames=lib_fullnames)

    @pytest.mark.usefixtures("_mock_ctypes")
    def test_brokenlib_invalidpath_workinglib(self):
        """
        Case 3: broken library + invalid path + working library.
        """
        lib_fullnames = [self.faked_libgmt1, self.invalid_path, self.loaded_libgmt]
        assert check_libgmt(load_libgmt(lib_fullnames=lib_fullnames)) is None

    @pytest.mark.usefixtures("_mock_ctypes")
    def test_invalidpath_brokenlib_workinglib(self):
        """
        Case 4: invalid path + broken library + working library.
        """
        lib_fullnames = [self.invalid_path, self.faked_libgmt1, self.loaded_libgmt]
        assert check_libgmt(load_libgmt(lib_fullnames=lib_fullnames)) is None

    @pytest.mark.usefixtures("_mock_ctypes")
    def test_workinglib_brokenlib_invalidpath(self):
        """
        Case 5: working library + broken library + invalid path.
        """
        lib_fullnames = [self.loaded_libgmt, self.faked_libgmt1, self.invalid_path]
        assert check_libgmt(load_libgmt(lib_fullnames=lib_fullnames)) is None

    @pytest.mark.usefixtures("_mock_ctypes")
    def test_brokenlib_brokenlib_workinglib(self):
        """
        Case 6: repeating broken libraries + working library.
        """
        lib_fullnames = [self.faked_libgmt1, self.faked_libgmt1, self.loaded_libgmt]
        assert check_libgmt(load_libgmt(lib_fullnames=lib_fullnames)) is None


class TestLibgmtCount:
    """
    Test that the GMT library is not repeatedly loaded in every session.
    """

    loaded_libgmt = load_libgmt()  # Load the GMT library and reuse it when necessary
    counter = 0  # Global counter for how many times ctypes.CDLL is called

    def _mock_ctypes_cdll_return(self, libname):  # noqa: ARG002
        """
        Mock ctypes.CDLL to count how many times the function is called.

        If ctypes.CDLL is called, the counter increases by one.
        """
        self.counter += 1  # Increase the counter
        return self.loaded_libgmt

    def test_libgmt_load_counter(self, monkeypatch):
        """
        Make sure that the GMT library is not loaded in every session.
        """
        # Monkeypatch the ctypes.CDLL function
        monkeypatch.setattr(ctypes, "CDLL", self._mock_ctypes_cdll_return)

        # Create two sessions and check the global counter
        with Session() as lib:
            _ = lib
        with Session() as lib:
            _ = lib
        assert self.counter == 0  # ctypes.CDLL is not called after two sessions.

        # Explicitly calling load_libgmt to make sure the mock function is correct
        load_libgmt()
        assert self.counter == 1
        load_libgmt()
        assert self.counter == 2


###############################################################################
# Test clib_full_names
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
        [shutil.which("gmt"), "--show-library"], encoding="utf-8"
    ).rstrip("\n")
    # On Windows, clib_full_names() returns paths with separator "\\",
    # but "gmt --show-library" returns paths with separator "/".
    # Use `str(PurePath(realpath)` to mimic the behavior of clib_full_names()
    return str(PurePath(lib_realpath))


def test_clib_full_names_gmt_library_path_undefined_path_empty(
    monkeypatch, gmt_lib_names
):
    """
    Make sure that clib_full_names() returns a generator with expected names when
    GMT_LIBRARY_PATH is undefined and PATH is empty.
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
    Make sure that clib_full_names() returns a generator with expected names when
    GMT_LIBRARY_PATH is defined and PATH is empty.
    """
    with monkeypatch.context() as mpatch:
        mpatch.setenv("GMT_LIBRARY_PATH", str(PurePath(gmt_lib_realpath).parent))
        mpatch.setenv("PATH", "")
        lib_fullpaths = clib_full_names()

        assert isinstance(lib_fullpaths, types.GeneratorType)
        assert list(lib_fullpaths) == [gmt_lib_realpath, *gmt_lib_names]


def test_clib_full_names_gmt_library_path_undefined_path_included(
    monkeypatch, gmt_lib_names, gmt_lib_realpath, gmt_bin_dir
):
    """
    Make sure that clib_full_names() returns a generator with expected names when
    GMT_LIBRARY_PATH is undefined and PATH includes GMT's bin path.
    """
    with monkeypatch.context() as mpatch:
        mpatch.delenv("GMT_LIBRARY_PATH", raising=False)
        mpatch.setenv("PATH", gmt_bin_dir, prepend=os.pathsep)
        lib_fullpaths = clib_full_names()
        assert isinstance(lib_fullpaths, types.GeneratorType)
        # Windows: find_library() searches the library in PATH, so one more
        npath = 2 if sys.platform == "win32" else 1
        assert list(lib_fullpaths) == [gmt_lib_realpath] * npath + gmt_lib_names


def test_clib_full_names_gmt_library_path_defined_path_included(
    monkeypatch, gmt_lib_names, gmt_lib_realpath, gmt_bin_dir
):
    """
    Make sure that clib_full_names() returns a generator with expected names when
    GMT_LIBRARY_PATH is defined and PATH includes GMT's bin path.
    """
    with monkeypatch.context() as mpatch:
        mpatch.setenv("GMT_LIBRARY_PATH", str(PurePath(gmt_lib_realpath).parent))
        mpatch.setenv("PATH", gmt_bin_dir, prepend=os.pathsep)
        lib_fullpaths = clib_full_names()

        assert isinstance(lib_fullpaths, types.GeneratorType)
        # Windows: find_library() searches the library in PATH, so one more
        npath = 3 if sys.platform == "win32" else 2
        assert list(lib_fullpaths) == [gmt_lib_realpath] * npath + gmt_lib_names


def test_clib_full_names_gmt_library_path_incorrect_path_included(
    monkeypatch, gmt_lib_names, gmt_lib_realpath, gmt_bin_dir
):
    """
    Make sure that clib_full_names() returns a generator with expected names when
    GMT_LIBRARY_PATH is defined but incorrect and PATH includes GMT's bin path.
    """
    with monkeypatch.context() as mpatch:
        mpatch.setenv("GMT_LIBRARY_PATH", "/not/a/valid/library/path")
        mpatch.setenv("PATH", gmt_bin_dir, prepend=os.pathsep)
        lib_fullpaths = clib_full_names()

        assert isinstance(lib_fullpaths, types.GeneratorType)
        # Windows: find_library() searches the library in PATH, so one more
        npath = 2 if sys.platform == "win32" else 1
        assert list(lib_fullpaths) == [gmt_lib_realpath] * npath + gmt_lib_names


###############################################################################
# Test get_gmt_version
def test_get_gmt_version():
    """
    Test if get_gmt_version returns a version string in major.minor.patch format.
    """
    version = get_gmt_version(load_libgmt())
    assert isinstance(version, str)
    assert len(version.split(".")) == 3  # In major.minor.patch format
    assert version.split(".")[0] == "6"  # Is GMT 6.x.x
