"""
Test the wrappers for the C API.
"""

from contextlib import contextmanager

import pytest
from packaging.version import Version
from pygmt import clib
from pygmt.clib import required_gmt_version
from pygmt.clib.session import FAMILIES, VIAS
from pygmt.exceptions import (
    GMTCLibError,
    GMTCLibNoSessionError,
    GMTInvalidInput,
    GMTVersionError,
)


@contextmanager
def mock(session, func, returns=None, mock_func=None):
    """
    Mock a GMT C API function to make it always return a given value.

    Used to test that exceptions are raised when API functions fail by producing a NULL
    pointer as output or non-zero status codes.

    Needed because it's not easy to get some API functions to fail without inducing a
    Segmentation Fault (which is a good thing because libgmt usually only fails with
    errors).
    """
    if mock_func is None:

        def mock_api_function(*args):  # noqa: ARG001
            """
            A mock GMT API function that always returns a given value.
            """
            return returns

        mock_func = mock_api_function

    get_libgmt_func = session.get_libgmt_func

    def mock_get_libgmt_func(name, argtypes=None, restype=None):
        """
        Return our mock function.
        """
        if name == func:
            return mock_func
        return get_libgmt_func(name, argtypes, restype)

    session.get_libgmt_func = mock_get_libgmt_func

    yield

    session.get_libgmt_func = get_libgmt_func


def test_getitem():
    """
    Test getting the GMT constants from the C library.
    """
    with clib.Session() as lib:
        for name in ["GMT_SESSION_EXTERNAL", "GMT_MODULE_CMD", "GMT_DOUBLE"]:
            assert lib[name] != -99999
        with pytest.raises(GMTCLibError):
            lib["A_WHOLE_LOT_OF_JUNK"]


def test_create_destroy_session():
    """
    Test that create and destroy session are called without errors.
    """
    # Create two session and make sure they are not pointing to the same memory
    session1 = clib.Session()
    session1.create(name="test_session1")
    assert session1.session_pointer is not None
    session2 = clib.Session()
    session2.create(name="test_session2")
    assert session2.session_pointer is not None
    assert session2.session_pointer != session1.session_pointer
    session1.destroy()
    session2.destroy()
    # Create and destroy a session twice
    ses = clib.Session()
    for __ in range(2):
        with pytest.raises(GMTCLibNoSessionError):
            _ = ses.session_pointer
        ses.create("session1")
        assert ses.session_pointer is not None
        ses.destroy()
        with pytest.raises(GMTCLibNoSessionError):
            _ = ses.session_pointer


def test_create_session_fails():
    """
    Check that an exception is raised when failing to create a session.
    """
    ses = clib.Session()
    with mock(ses, "GMT_Create_Session", returns=None):
        with pytest.raises(GMTCLibError):
            ses.create("test-session-name")
    # Should fail if trying to create a session before destroying the old one.
    ses.create("test1")
    with pytest.raises(GMTCLibError):
        ses.create("test2")


def test_destroy_session_fails():
    """
    Fail to destroy session when given bad input.
    """
    ses = clib.Session()
    with pytest.raises(GMTCLibNoSessionError):
        ses.destroy()
    ses.create("test-session")
    with mock(ses, "GMT_Destroy_Session", returns=1):
        with pytest.raises(GMTCLibError):
            ses.destroy()
    ses.destroy()


def test_method_no_session():
    """
    Fails when not in a session.
    """
    # Create an instance of Session without "with" so no session is created.
    lib = clib.Session()
    with pytest.raises(GMTCLibNoSessionError):
        lib.call_module("gmtdefaults", [])
    with pytest.raises(GMTCLibNoSessionError):
        _ = lib.session_pointer


def test_parse_constant_single():
    """
    Parsing a single family argument correctly.
    """
    lib = clib.Session()
    for family in FAMILIES:
        parsed = lib._parse_constant(family, valid=FAMILIES)
        assert parsed == lib[family]


def test_parse_constant_composite():
    """
    Parsing a composite constant argument (separated by |) correctly.
    """
    lib = clib.Session()
    test_cases = ((family, via) for family in FAMILIES for via in VIAS)
    for family, via in test_cases:
        composite = f"{family}|{via}"
        expected = lib[family] + lib[via]
        parsed = lib._parse_constant(composite, valid=FAMILIES, valid_modifiers=VIAS)
        assert parsed == expected


def test_parse_constant_fails():
    """
    Check if the function fails when given bad input.
    """
    lib = clib.Session()
    test_cases = [
        "SOME_random_STRING",
        "GMT_IS_DATASET|GMT_VIA_MATRIX|GMT_VIA_VECTOR",
        "GMT_IS_DATASET|NOT_A_PROPER_VIA",
        "NOT_A_PROPER_FAMILY|GMT_VIA_MATRIX",
        "NOT_A_PROPER_FAMILY|ALSO_INVALID",
    ]
    for test_case in test_cases:
        with pytest.raises(GMTInvalidInput):
            lib._parse_constant(test_case, valid=FAMILIES, valid_modifiers=VIAS)

    # Should also fail if not given valid modifiers but is using them anyway.
    # This should work...
    lib._parse_constant(
        "GMT_IS_DATASET|GMT_VIA_MATRIX", valid=FAMILIES, valid_modifiers=VIAS
    )
    # But this shouldn't.
    with pytest.raises(GMTInvalidInput):
        lib._parse_constant(
            "GMT_IS_DATASET|GMT_VIA_MATRIX", valid=FAMILIES, valid_modifiers=None
        )


def test_get_default():
    """
    Make sure get_default works without crashing and gives reasonable results.
    """
    with clib.Session() as lib:
        assert lib.get_default("API_GRID_LAYOUT") in {"rows", "columns"}
        assert int(lib.get_default("API_CORES")) >= 1
        assert Version(lib.get_default("API_VERSION")) >= Version(required_gmt_version)
        assert lib.get_default("PROJ_LENGTH_UNIT") == "cm"


def test_get_default_fails():
    """
    Make sure get_default raises an exception for invalid names.
    """
    with clib.Session() as lib:
        with pytest.raises(GMTCLibError):
            lib.get_default("NOT_A_VALID_NAME")


def test_info_dict():
    """
    Make sure the clib.Session.info dict is working.
    """
    # Check if there are no errors or segfaults from getting all of the
    # properties.
    with clib.Session() as lib:
        assert lib.info

    # Mock GMT_Get_Default to return always the same string
    def mock_defaults(api, name, value):  # noqa: ARG001
        """
        Put 'bla' in the value buffer.
        """
        if name == b"API_VERSION":
            value.value = b"1.2.3"
        else:
            value.value = b"bla"
        return 0

    ses = clib.Session()
    ses.create("test-session")
    with mock(ses, "GMT_Get_Default", mock_func=mock_defaults):
        # Check for an empty dictionary
        assert ses.info
        for key, value in ses.info.items():
            if key == "version":
                assert value == "1.2.3"
            else:
                assert value == "bla"
    ses.destroy()


def test_fails_for_wrong_version(monkeypatch):
    """
    Make sure that importing clib raise an exception if GMT is too old.
    """
    import importlib

    with monkeypatch.context() as mpatch:
        # Make sure the current GMT major version is 6.
        assert clib.__gmt_version__.split(".")[0] == "6"

        # Monkeypatch the version string returned by pygmt.clib.loading.get_gmt_version.
        mpatch.setattr(clib.loading, "get_gmt_version", lambda libgmt: "5.4.3")  # noqa: ARG005

        # Reload clib.session and check the __gmt_version__ string.
        importlib.reload(clib.session)
        assert clib.session.__gmt_version__ == "5.4.3"

        # Should raise an exception when pygmt.clib is loaded/reloaded.
        with pytest.raises(GMTVersionError):
            importlib.reload(clib)
        assert clib.__gmt_version__ == "5.4.3"  # Make sure it's still the old version
