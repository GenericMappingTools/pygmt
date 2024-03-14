"""
Test the wrappers for the C API.
"""

import os
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import numpy.testing as npt
import pytest
import xarray as xr
from packaging.version import Version
from pygmt import Figure, clib
from pygmt.clib.conversion import dataarray_to_matrix
from pygmt.clib.session import FAMILIES, VIAS
from pygmt.exceptions import (
    GMTCLibError,
    GMTCLibNoSessionError,
    GMTInvalidInput,
    GMTVersionError,
)
from pygmt.helpers import GMTTempFile

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


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
    Test that I can get correct constants from the C lib.
    """
    ses = clib.Session()
    assert ses["GMT_SESSION_EXTERNAL"] != -99999
    assert ses["GMT_MODULE_CMD"] != -99999
    assert ses["GMT_PAD_DEFAULT"] != -99999
    assert ses["GMT_DOUBLE"] != -99999
    with pytest.raises(GMTCLibError):
        ses["A_WHOLE_LOT_OF_JUNK"]


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


@pytest.mark.benchmark
def test_call_module():
    """
    Run a command to see if call_module works.
    """
    data_fname = os.path.join(TEST_DATA_DIR, "points.txt")
    out_fname = "test_call_module.txt"
    with clib.Session() as lib:
        with GMTTempFile() as out_fname:
            lib.call_module("info", f"{data_fname} -C ->{out_fname.name}")
            assert Path(out_fname.name).stat().st_size > 0
            output = out_fname.read().strip()
            assert output == "11.5309 61.7074 -2.9289 7.8648 0.1412 0.9338"


def test_call_module_invalid_arguments():
    """
    Fails for invalid module arguments.
    """
    with clib.Session() as lib:
        with pytest.raises(GMTCLibError):
            lib.call_module("info", "bogus-data.bla")


def test_call_module_invalid_name():
    """
    Fails when given bad input.
    """
    with clib.Session() as lib:
        with pytest.raises(GMTCLibError):
            lib.call_module("meh", "")


def test_call_module_error_message():
    """
    Check is the GMT error message was captured.
    """
    with clib.Session() as lib:
        with pytest.raises(GMTCLibError) as exc_info:
            lib.call_module("info", "bogus-data.bla")
        assert "Module 'info' failed with status code" in exc_info.value.args[0]
        assert (
            "gmtinfo [ERROR]: Cannot find file bogus-data.bla" in exc_info.value.args[0]
        )


def test_method_no_session():
    """
    Fails when not in a session.
    """
    # Create an instance of Session without "with" so no session is created.
    lib = clib.Session()
    with pytest.raises(GMTCLibNoSessionError):
        lib.call_module("gmtdefaults", "")
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


def test_create_data_dataset():
    """
    Run the function to make sure it doesn't fail badly.
    """
    with clib.Session() as lib:
        # Dataset from vectors
        data_vector = lib.create_data(
            family="GMT_IS_DATASET|GMT_VIA_VECTOR",
            geometry="GMT_IS_POINT",
            mode="GMT_CONTAINER_ONLY",
            dim=[10, 20, 1, 0],  # columns, rows, layers, dtype
        )
        # Dataset from matrices
        data_matrix = lib.create_data(
            family="GMT_IS_DATASET|GMT_VIA_MATRIX",
            geometry="GMT_IS_POINT",
            mode="GMT_CONTAINER_ONLY",
            dim=[10, 20, 1, 0],
        )
        assert data_vector != data_matrix


def test_create_data_grid_dim():
    """
    Create a grid ignoring range and inc.
    """
    with clib.Session() as lib:
        # Grids from matrices using dim
        lib.create_data(
            family="GMT_IS_GRID|GMT_VIA_MATRIX",
            geometry="GMT_IS_SURFACE",
            mode="GMT_CONTAINER_ONLY",
            dim=[10, 20, 1, 0],
        )


def test_create_data_grid_range():
    """
    Create a grid specifying range and inc instead of dim.
    """
    with clib.Session() as lib:
        # Grids from matrices using range and int
        lib.create_data(
            family="GMT_IS_GRID|GMT_VIA_MATRIX",
            geometry="GMT_IS_SURFACE",
            mode="GMT_CONTAINER_ONLY",
            ranges=[150.0, 250.0, -20.0, 20.0],
            inc=[0.1, 0.2],
        )


def test_create_data_fails():
    """
    Check that create_data raises exceptions for invalid input and output.
    """
    # Passing in invalid mode
    with pytest.raises(GMTInvalidInput):
        with clib.Session() as lib:
            lib.create_data(
                family="GMT_IS_DATASET",
                geometry="GMT_IS_SURFACE",
                mode="Not_a_valid_mode",
                dim=[0, 0, 1, 0],
                ranges=[150.0, 250.0, -20.0, 20.0],
                inc=[0.1, 0.2],
            )
    # Passing in invalid geometry
    with pytest.raises(GMTInvalidInput):
        with clib.Session() as lib:
            lib.create_data(
                family="GMT_IS_GRID",
                geometry="Not_a_valid_geometry",
                mode="GMT_CONTAINER_ONLY",
                dim=[0, 0, 1, 0],
                ranges=[150.0, 250.0, -20.0, 20.0],
                inc=[0.1, 0.2],
            )

    # If the data pointer returned is None (NULL pointer)
    with clib.Session() as lib:
        with mock(lib, "GMT_Create_Data", returns=None):
            with pytest.raises(GMTCLibError):
                lib.create_data(
                    family="GMT_IS_DATASET",
                    geometry="GMT_IS_SURFACE",
                    mode="GMT_CONTAINER_ONLY",
                    dim=[11, 10, 2, 0],
                )


def test_extract_region_fails():
    """
    Check that extract region fails if nothing has been plotted.
    """
    Figure()
    with pytest.raises(GMTCLibError):
        with clib.Session() as lib:
            lib.extract_region()


def test_extract_region_two_figures():
    """
    Extract region should handle multiple figures existing at the same time.
    """
    # Make two figures before calling extract_region to make sure that it's
    # getting from the current figure, not the last figure.
    fig1 = Figure()
    region1 = np.array([0, 10, -20, -10])
    fig1.coast(region=region1, projection="M6i", frame=True, land="black")

    fig2 = Figure()
    fig2.basemap(region="US.HI+r5", projection="M6i", frame=True)

    # Activate the first figure and extract the region from it
    # Use in a different session to avoid any memory problems.
    with clib.Session() as lib:
        lib.call_module("figure", f"{fig1._name} -")
    with clib.Session() as lib:
        wesn1 = lib.extract_region()
        npt.assert_allclose(wesn1, region1)

    # Now try it with the second one
    with clib.Session() as lib:
        lib.call_module("figure", f"{fig2._name} -")
    with clib.Session() as lib:
        wesn2 = lib.extract_region()
        npt.assert_allclose(wesn2, np.array([-165.0, -150.0, 15.0, 25.0]))


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


@pytest.mark.benchmark
def test_dataarray_to_matrix_works():
    """
    Check that dataarray_to_matrix returns correct output.
    """
    data = np.diag(v=np.arange(3))
    x = np.linspace(start=0, stop=4, num=3)
    y = np.linspace(start=5, stop=9, num=3)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])

    matrix, region, inc = dataarray_to_matrix(grid)
    npt.assert_allclose(actual=matrix, desired=np.flipud(data))
    npt.assert_allclose(actual=region, desired=[x.min(), x.max(), y.min(), y.max()])
    npt.assert_allclose(actual=inc, desired=[x[1] - x[0], y[1] - y[0]])


def test_dataarray_to_matrix_negative_x_increment():
    """
    Check if dataarray_to_matrix returns correct output with flipped x.
    """
    data = np.diag(v=np.arange(3))
    x = np.linspace(start=4, stop=0, num=3)
    y = np.linspace(start=5, stop=9, num=3)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])

    matrix, region, inc = dataarray_to_matrix(grid)
    npt.assert_allclose(actual=matrix, desired=np.flip(data, axis=(0, 1)))
    npt.assert_allclose(actual=region, desired=[x.min(), x.max(), y.min(), y.max()])
    npt.assert_allclose(actual=inc, desired=[abs(x[1] - x[0]), abs(y[1] - y[0])])


def test_dataarray_to_matrix_negative_y_increment():
    """
    Check that dataarray_to_matrix returns correct output with flipped y.
    """
    data = np.diag(v=np.arange(3))
    x = np.linspace(start=0, stop=4, num=3)
    y = np.linspace(start=9, stop=5, num=3)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])

    matrix, region, inc = dataarray_to_matrix(grid)
    npt.assert_allclose(actual=matrix, desired=data)
    npt.assert_allclose(actual=region, desired=[x.min(), x.max(), y.min(), y.max()])
    npt.assert_allclose(actual=inc, desired=[abs(x[1] - x[0]), abs(y[1] - y[0])])


def test_dataarray_to_matrix_negative_x_and_y_increment():
    """
    Check that dataarray_to_matrix returns correct output with flipped x/y.
    """
    data = np.diag(v=np.arange(3))
    x = np.linspace(start=4, stop=0, num=3)
    y = np.linspace(start=9, stop=5, num=3)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])

    matrix, region, inc = dataarray_to_matrix(grid)
    npt.assert_allclose(actual=matrix, desired=np.fliplr(data))
    npt.assert_allclose(actual=region, desired=[x.min(), x.max(), y.min(), y.max()])
    npt.assert_allclose(actual=inc, desired=[abs(x[1] - x[0]), abs(y[1] - y[0])])


def test_dataarray_to_matrix_dims_fails():
    """
    Check that it fails for > 2 dims.
    """
    # Make a 3-D regular grid
    data = np.ones((10, 12, 11), dtype="float32")
    x = np.arange(11)
    y = np.arange(12)
    z = np.arange(10)
    grid = xr.DataArray(data, coords=[("z", z), ("y", y), ("x", x)])
    with pytest.raises(GMTInvalidInput):
        dataarray_to_matrix(grid)


def test_dataarray_to_matrix_irregular_inc_warning():
    """
    Check that it warns for variable increments, see also
    https://github.com/GenericMappingTools/pygmt/issues/1468.
    """
    data = np.ones((4, 5), dtype="float64")
    x = np.linspace(0, 1, 5)
    y = np.logspace(2, 3, 4)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])
    with pytest.warns(expected_warning=RuntimeWarning) as record:
        dataarray_to_matrix(grid)
        assert len(record) == 1


def test_dataarray_to_matrix_zero_inc_fails():
    """
    Check that dataarray_to_matrix fails for zero increments grid.
    """
    data = np.ones((5, 5), dtype="float32")
    x = np.linspace(0, 1, 5)
    y = np.zeros_like(x)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])
    with pytest.raises(GMTInvalidInput):
        dataarray_to_matrix(grid)

    y = np.linspace(0, 1, 5)
    x = np.zeros_like(x)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])
    with pytest.raises(GMTInvalidInput):
        dataarray_to_matrix(grid)


def test_get_default():
    """
    Make sure get_default works without crashing and gives reasonable results.
    """
    with clib.Session() as lib:
        assert lib.get_default("API_GRID_LAYOUT") in ["rows", "columns"]
        assert int(lib.get_default("API_CORES")) >= 1
        assert Version(lib.get_default("API_VERSION")) >= Version("6.3.0")


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


def test_fails_for_wrong_version():
    """
    Make sure the clib.Session raises an exception if GMT is too old.
    """

    # Mock GMT_Get_Default to return an old version
    def mock_defaults(api, name, value):  # noqa: ARG001
        """
        Return an old version.
        """
        if name == b"API_VERSION":
            value.value = b"5.4.3"
        else:
            value.value = b"bla"
        return 0

    lib = clib.Session()
    with mock(lib, "GMT_Get_Default", mock_func=mock_defaults):
        with pytest.raises(GMTVersionError):
            with lib:
                assert lib.info["version"] != "5.4.3"
    # Make sure the session is closed when the exception is raised.
    with pytest.raises(GMTCLibNoSessionError):
        assert lib.session_pointer
