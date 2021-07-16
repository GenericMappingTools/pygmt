# pylint: disable=protected-access
"""
Test the wrappers for the C API.
"""
import os
from contextlib import contextmanager

import numpy as np
import numpy.testing as npt
import pandas as pd
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

with clib.Session() as _lib:
    gmt_version = Version(_lib.info["version"])


@contextmanager
def mock(session, func, returns=None, mock_func=None):
    """
    Mock a GMT C API function to make it always return a given value.

    Used to test that exceptions are raised when API functions fail by
    producing a NULL pointer as output or non-zero status codes.

    Needed because it's not easy to get some API functions to fail without
    inducing a Segmentation Fault (which is a good thing because libgmt usually
    only fails with errors).
    """
    if mock_func is None:

        def mock_api_function(*args):  # pylint: disable=unused-argument
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

    setattr(session, "get_libgmt_func", mock_get_libgmt_func)

    yield

    setattr(session, "get_libgmt_func", get_libgmt_func)


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
        ses["A_WHOLE_LOT_OF_JUNK"]  # pylint: disable=pointless-statement


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
            ses.session_pointer  # pylint: disable=pointless-statement
        ses.create("session1")
        assert ses.session_pointer is not None
        ses.destroy()
        with pytest.raises(GMTCLibNoSessionError):
            ses.session_pointer  # pylint: disable=pointless-statement


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


def test_call_module():
    """
    Run a command to see if call_module works.
    """
    data_fname = os.path.join(TEST_DATA_DIR, "points.txt")
    out_fname = "test_call_module.txt"
    with clib.Session() as lib:
        with GMTTempFile() as out_fname:
            lib.call_module("info", "{} -C ->{}".format(data_fname, out_fname.name))
            assert os.path.exists(out_fname.name)
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
        try:
            lib.call_module("info", "bogus-data.bla")
        except GMTCLibError as error:
            assert "Module 'info' failed with status code" in str(error)
            assert "gmtinfo [ERROR]: Cannot find file bogus-data.bla" in str(error)


def test_method_no_session():
    """
    Fails when not in a session.
    """
    # Create an instance of Session without "with" so no session is created.
    lib = clib.Session()
    with pytest.raises(GMTCLibNoSessionError):
        lib.call_module("gmtdefaults", "")
    with pytest.raises(GMTCLibNoSessionError):
        lib.session_pointer  # pylint: disable=pointless-statement


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
        composite = "|".join([family, via])
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
    with pytest.raises(GMTCLibError):
        with clib.Session() as lib:
            with mock(lib, "GMT_Create_Data", returns=None):
                lib.create_data(
                    family="GMT_IS_DATASET",
                    geometry="GMT_IS_SURFACE",
                    mode="GMT_CONTAINER_ONLY",
                    dim=[11, 10, 2, 0],
                )


def test_virtual_file():
    """
    Test passing in data via a virtual file with a Dataset.
    """
    dtypes = "float32 float64 int32 int64 uint32 uint64".split()
    shape = (5, 3)
    for dtype in dtypes:
        with clib.Session() as lib:
            family = "GMT_IS_DATASET|GMT_VIA_MATRIX"
            geometry = "GMT_IS_POINT"
            dataset = lib.create_data(
                family=family,
                geometry=geometry,
                mode="GMT_CONTAINER_ONLY",
                dim=[shape[1], shape[0], 1, 0],  # columns, rows, layers, dtype
            )
            data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
            lib.put_matrix(dataset, matrix=data)
            # Add the dataset to a virtual file and pass it along to gmt info
            vfargs = (family, geometry, "GMT_IN|GMT_IS_REFERENCE", dataset)
            with lib.open_virtual_file(*vfargs) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", "{} ->{}".format(vfile, outfile.name))
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join(
                ["<{:.0f}/{:.0f}>".format(col.min(), col.max()) for col in data.T]
            )
            expected = "<matrix memory>: N = {}\t{}\n".format(shape[0], bounds)
            assert output == expected


def test_virtual_file_fails():
    """
    Check that opening and closing virtual files raises an exception for non-
    zero return codes.
    """
    vfargs = (
        "GMT_IS_DATASET|GMT_VIA_MATRIX",
        "GMT_IS_POINT",
        "GMT_IN|GMT_IS_REFERENCE",
        None,
    )

    # Mock Open_VirtualFile to test the status check when entering the context.
    # If the exception is raised, the code won't get to the closing of the
    # virtual file.
    with clib.Session() as lib, mock(lib, "GMT_Open_VirtualFile", returns=1):
        with pytest.raises(GMTCLibError):
            with lib.open_virtual_file(*vfargs):
                print("Should not get to this code")

    # Test the status check when closing the virtual file
    # Mock the opening to return 0 (success) so that we don't open a file that
    # we won't close later.
    with clib.Session() as lib, mock(lib, "GMT_Open_VirtualFile", returns=0), mock(
        lib, "GMT_Close_VirtualFile", returns=1
    ):
        with pytest.raises(GMTCLibError):
            with lib.open_virtual_file(*vfargs):
                pass
            print("Shouldn't get to this code either")


def test_virtual_file_bad_direction():
    """
    Test passing an invalid direction argument.
    """
    with clib.Session() as lib:
        vfargs = (
            "GMT_IS_DATASET|GMT_VIA_MATRIX",
            "GMT_IS_POINT",
            "GMT_IS_GRID",  # The invalid direction argument
            0,
        )
        with pytest.raises(GMTInvalidInput):
            with lib.open_virtual_file(*vfargs):
                print("This should have failed")


def test_virtualfile_from_vectors():
    """
    Test the automation for transforming vectors to virtual file dataset.
    """
    dtypes = "float32 float64 int32 int64 uint32 uint64".split()
    size = 10
    for dtype in dtypes:
        x = np.arange(size, dtype=dtype)
        y = np.arange(size, size * 2, 1, dtype=dtype)
        z = np.arange(size * 2, size * 3, 1, dtype=dtype)
        with clib.Session() as lib:
            with lib.virtualfile_from_vectors(x, y, z) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", "{} ->{}".format(vfile, outfile.name))
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join(
                ["<{:.0f}/{:.0f}>".format(i.min(), i.max()) for i in (x, y, z)]
            )
            expected = "<vector memory>: N = {}\t{}\n".format(size, bounds)
            assert output == expected


@pytest.mark.parametrize("dtype", [str, object])
def test_virtualfile_from_vectors_one_string_or_object_column(dtype):
    """
    Test passing in one column with string or object dtype into virtual file
    dataset.
    """
    size = 5
    x = np.arange(size, dtype=np.int32)
    y = np.arange(size, size * 2, 1, dtype=np.int32)
    strings = np.array(["a", "bc", "defg", "hijklmn", "opqrst"], dtype=dtype)
    with clib.Session() as lib:
        with lib.virtualfile_from_vectors(x, y, strings) as vfile:
            with GMTTempFile() as outfile:
                lib.call_module("convert", f"{vfile} ->{outfile.name}")
                output = outfile.read(keep_tabs=True)
        expected = "".join(f"{i}\t{j}\t{k}\n" for i, j, k in zip(x, y, strings))
        assert output == expected


@pytest.mark.parametrize("dtype", [str, object])
def test_virtualfile_from_vectors_two_string_or_object_columns(dtype):
    """
    Test passing in two columns of string or object dtype into virtual file
    dataset.
    """
    size = 5
    x = np.arange(size, dtype=np.int32)
    y = np.arange(size, size * 2, 1, dtype=np.int32)
    strings1 = np.array(["a", "bc", "def", "ghij", "klmno"], dtype=dtype)
    strings2 = np.array(["pqrst", "uvwx", "yz!", "@#", "$"], dtype=dtype)
    with clib.Session() as lib:
        with lib.virtualfile_from_vectors(x, y, strings1, strings2) as vfile:
            with GMTTempFile() as outfile:
                lib.call_module("convert", f"{vfile} ->{outfile.name}")
                output = outfile.read(keep_tabs=True)
        expected = "".join(
            f"{h}\t{i}\t{j} {k}\n" for h, i, j, k in zip(x, y, strings1, strings2)
        )
        assert output == expected


def test_virtualfile_from_vectors_transpose():
    """
    Test transforming matrix columns to virtual file dataset.
    """
    dtypes = "float32 float64 int32 int64 uint32 uint64".split()
    shape = (7, 5)
    for dtype in dtypes:
        data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
        with clib.Session() as lib:
            with lib.virtualfile_from_vectors(*data.T) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", "{} -C ->{}".format(vfile, outfile.name))
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join(
                ["{:.0f}\t{:.0f}".format(col.min(), col.max()) for col in data.T]
            )
            expected = "{}\n".format(bounds)
            assert output == expected


def test_virtualfile_from_vectors_diff_size():
    """
    Test the function fails for arrays of different sizes.
    """
    x = np.arange(5)
    y = np.arange(6)
    with clib.Session() as lib:
        with pytest.raises(GMTInvalidInput):
            with lib.virtualfile_from_vectors(x, y):
                print("This should have failed")


def test_virtualfile_from_matrix():
    """
    Test transforming a matrix to virtual file dataset.
    """
    dtypes = "float32 float64 int32 int64 uint32 uint64".split()
    shape = (7, 5)
    for dtype in dtypes:
        data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
        with clib.Session() as lib:
            with lib.virtualfile_from_matrix(data) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", "{} ->{}".format(vfile, outfile.name))
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join(
                ["<{:.0f}/{:.0f}>".format(col.min(), col.max()) for col in data.T]
            )
            expected = "<matrix memory>: N = {}\t{}\n".format(shape[0], bounds)
            assert output == expected


def test_virtualfile_from_matrix_slice():
    """
    Test transforming a slice of a larger array to virtual file dataset.
    """
    dtypes = "float32 float64 int32 int64 uint32 uint64".split()
    shape = (10, 6)
    for dtype in dtypes:
        full_data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
        rows = 5
        cols = 3
        data = full_data[:rows, :cols]
        with clib.Session() as lib:
            with lib.virtualfile_from_matrix(data) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", "{} ->{}".format(vfile, outfile.name))
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join(
                ["<{:.0f}/{:.0f}>".format(col.min(), col.max()) for col in data.T]
            )
            expected = "<matrix memory>: N = {}\t{}\n".format(rows, bounds)
            assert output == expected


def test_virtualfile_from_vectors_pandas():
    """
    Pass vectors to a dataset using pandas Series.
    """
    dtypes = "float32 float64 int32 int64 uint32 uint64".split()
    size = 13
    for dtype in dtypes:
        data = pd.DataFrame(
            data=dict(
                x=np.arange(size, dtype=dtype),
                y=np.arange(size, size * 2, 1, dtype=dtype),
                z=np.arange(size * 2, size * 3, 1, dtype=dtype),
            )
        )
        with clib.Session() as lib:
            with lib.virtualfile_from_vectors(data.x, data.y, data.z) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", "{} ->{}".format(vfile, outfile.name))
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join(
                [
                    "<{:.0f}/{:.0f}>".format(i.min(), i.max())
                    for i in (data.x, data.y, data.z)
                ]
            )
            expected = "<vector memory>: N = {}\t{}\n".format(size, bounds)
            assert output == expected


def test_virtualfile_from_vectors_arraylike():
    """
    Pass array-like vectors to a dataset.
    """
    size = 13
    x = list(range(0, size, 1))
    y = tuple(range(size, size * 2, 1))
    z = range(size * 2, size * 3, 1)
    with clib.Session() as lib:
        with lib.virtualfile_from_vectors(x, y, z) as vfile:
            with GMTTempFile() as outfile:
                lib.call_module("info", "{} ->{}".format(vfile, outfile.name))
                output = outfile.read(keep_tabs=True)
        bounds = "\t".join(
            ["<{:.0f}/{:.0f}>".format(min(i), max(i)) for i in (x, y, z)]
        )
        expected = "<vector memory>: N = {}\t{}\n".format(size, bounds)
        assert output == expected


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
        lib.call_module("figure", "{} -".format(fig1._name))
    with clib.Session() as lib:
        wesn1 = lib.extract_region()
        npt.assert_allclose(wesn1, region1)

    # Now try it with the second one
    with clib.Session() as lib:
        lib.call_module("figure", "{} -".format(fig2._name))
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
    # Make a 3D regular grid
    data = np.ones((10, 12, 11), dtype="float32")
    x = np.arange(11)
    y = np.arange(12)
    z = np.arange(10)
    grid = xr.DataArray(data, coords=[("z", z), ("y", y), ("x", x)])
    with pytest.raises(GMTInvalidInput):
        dataarray_to_matrix(grid)


def test_dataarray_to_matrix_inc_fails():
    """
    Check that it fails for variable increments.
    """
    data = np.ones((4, 5), dtype="float64")
    x = np.linspace(0, 1, 5)
    y = np.logspace(2, 3, 4)
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
        assert Version(lib.get_default("API_VERSION")) >= Version("6.2.0")


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
    def mock_defaults(api, name, value):  # pylint: disable=unused-argument
        """
        Put 'bla' in the value buffer.
        """
        value.value = b"bla"
        return 0

    ses = clib.Session()
    ses.create("test-session")
    with mock(ses, "GMT_Get_Default", mock_func=mock_defaults):
        # Check for an empty dictionary
        assert ses.info
        for value in ses.info.values():
            assert value == "bla"
    ses.destroy()


def test_fails_for_wrong_version():
    """
    Make sure the clib.Session raises an exception if GMT is too old.
    """

    # Mock GMT_Get_Default to return an old version
    def mock_defaults(api, name, value):  # pylint: disable=unused-argument
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
