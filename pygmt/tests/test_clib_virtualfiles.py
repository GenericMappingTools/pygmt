"""
Test the C API functions related to virtual files.
"""
import os
from importlib.util import find_spec
from itertools import product

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from pygmt import clib
from pygmt.exceptions import GMTCLibError, GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.tests.test_clib import mock

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the point data from the test file.
    """
    return np.loadtxt(POINTS_DATA)


@pytest.fixture(scope="module", name="dtypes")
def fixture_dtypes():
    """
    List of supported numpy dtypes.
    """
    return "int8 int16 int32 int64 uint8 uint16 uint32 uint64 float32 float64".split()


@pytest.fixture(scope="module", name="dtypes_pandas")
def fixture_dtypes_pandas(dtypes):
    """
    List of supported pandas dtypes.
    """
    dtypes_pandas = dtypes.copy()

    if find_spec("pyarrow") is not None:
        dtypes_pandas.extend([f"{dtype}[pyarrow]" for dtype in dtypes_pandas])

    return tuple(dtypes_pandas)


@pytest.mark.benchmark
def test_virtual_file(dtypes):
    """
    Test passing in data via a virtual file with a Dataset.
    """
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
                    lib.call_module("info", f"{vfile} ->{outfile.name}")
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join([f"<{col.min():.0f}/{col.max():.0f}>" for col in data.T])
            expected = f"<matrix memory>: N = {shape[0]}\t{bounds}\n"
            assert output == expected


def test_virtual_file_fails():
    """
    Check that opening and closing virtual files raises an exception for non- zero
    return codes.
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
                pass

    # Test the status check when closing the virtual file
    # Mock the opening to return 0 (success) so that we don't open a file that
    # we won't close later.
    with clib.Session() as lib, mock(lib, "GMT_Open_VirtualFile", returns=0), mock(
        lib, "GMT_Close_VirtualFile", returns=1
    ):
        with pytest.raises(GMTCLibError):
            with lib.open_virtual_file(*vfargs):
                pass


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
                pass


@pytest.mark.benchmark
@pytest.mark.parametrize(
    ("array_func", "kind"),
    [(np.array, "matrix"), (pd.DataFrame, "vector"), (xr.Dataset, "vector")],
)
def test_virtualfile_from_data_required_z_matrix(array_func, kind):
    """
    Test that function works when third z column in a matrix is needed and provided.
    """
    shape = (5, 3)
    dataframe = pd.DataFrame(
        data=np.arange(shape[0] * shape[1]).reshape(shape), columns=["x", "y", "z"]
    )
    data = array_func(dataframe)
    with clib.Session() as lib:
        with lib.virtualfile_from_data(
            data=data, required_z=True, check_kind="vector"
        ) as vfile:
            with GMTTempFile() as outfile:
                lib.call_module("info", f"{vfile} ->{outfile.name}")
                output = outfile.read(keep_tabs=True)
        bounds = "\t".join(
            [
                f"<{i.min():.0f}/{i.max():.0f}>"
                for i in (dataframe.x, dataframe.y, dataframe.z)
            ]
        )
        expected = f"<{kind} memory>: N = {shape[0]}\t{bounds}\n"
        assert output == expected


def test_virtualfile_from_data_required_z_matrix_missing():
    """
    Test that function fails when third z column in a matrix is needed but not provided.
    """
    data = np.ones((5, 2))
    with clib.Session() as lib:
        with pytest.raises(GMTInvalidInput):
            with lib.virtualfile_from_data(
                data=data, required_z=True, check_kind="vector"
            ):
                pass


def test_virtualfile_from_data_fail_non_valid_data(data):
    """
    Should raise an exception if too few or too much data is given.
    """
    # Test all combinations where at least one data variable
    # is not given in the x, y case:
    for variable in product([None, data[:, 0]], repeat=2):
        # Filter one valid configuration:
        if not any(item is None for item in variable):
            continue
        with clib.Session() as lib:
            with pytest.raises(GMTInvalidInput):
                lib.virtualfile_from_data(x=variable[0], y=variable[1])

    # Test all combinations where at least one data variable
    # is not given in the x, y, z case:
    for variable in product([None, data[:, 0]], repeat=3):
        # Filter one valid configuration:
        if not any(item is None for item in variable):
            continue
        with clib.Session() as lib:
            with pytest.raises(GMTInvalidInput):
                lib.virtualfile_from_data(
                    x=variable[0], y=variable[1], z=variable[2], required_z=True
                )

    # Should also fail if given too much data
    with clib.Session() as lib:
        with pytest.raises(GMTInvalidInput):
            lib.virtualfile_from_data(
                x=data[:, 0],
                y=data[:, 1],
                z=data[:, 2],
                data=data,
            )


@pytest.mark.benchmark
def test_virtualfile_from_vectors(dtypes):
    """
    Test the automation for transforming vectors to virtual file dataset.
    """
    size = 10
    for dtype in dtypes:
        x = np.arange(size, dtype=dtype)
        y = np.arange(size, size * 2, 1, dtype=dtype)
        z = np.arange(size * 2, size * 3, 1, dtype=dtype)
        with clib.Session() as lib:
            with lib.virtualfile_from_vectors(x, y, z) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", f"{vfile} ->{outfile.name}")
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join([f"<{i.min():.0f}/{i.max():.0f}>" for i in (x, y, z)])
            expected = f"<vector memory>: N = {size}\t{bounds}\n"
            assert output == expected


@pytest.mark.benchmark
@pytest.mark.parametrize("dtype", [str, object])
def test_virtualfile_from_vectors_one_string_or_object_column(dtype):
    """
    Test passing in one column with string or object dtype into virtual file dataset.
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
    Test passing in two columns of string or object dtype into virtual file dataset.
    """
    size = 5
    x = np.arange(size, dtype=np.int32)
    y = np.arange(size, size * 2, 1, dtype=np.int32)
    # Catch bug in https://github.com/GenericMappingTools/pygmt/pull/2719
    strings1 = np.array(["a", "bc", "def", "ghij", "klmnolooong"], dtype=dtype)
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


def test_virtualfile_from_vectors_transpose(dtypes):
    """
    Test transforming matrix columns to virtual file dataset.
    """
    shape = (7, 5)
    for dtype in dtypes:
        data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
        with clib.Session() as lib:
            with lib.virtualfile_from_vectors(*data.T) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", f"{vfile} -C ->{outfile.name}")
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join([f"{col.min():.0f}\t{col.max():.0f}" for col in data.T])
            expected = f"{bounds}\n"
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
                pass


@pytest.mark.benchmark
def test_virtualfile_from_matrix(dtypes):
    """
    Test transforming a matrix to virtual file dataset.
    """
    shape = (7, 5)
    for dtype in dtypes:
        data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
        with clib.Session() as lib:
            with lib.virtualfile_from_matrix(data) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", f"{vfile} ->{outfile.name}")
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join([f"<{col.min():.0f}/{col.max():.0f}>" for col in data.T])
            expected = f"<matrix memory>: N = {shape[0]}\t{bounds}\n"
            assert output == expected


def test_virtualfile_from_matrix_slice(dtypes):
    """
    Test transforming a slice of a larger array to virtual file dataset.
    """
    shape = (10, 6)
    for dtype in dtypes:
        full_data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
        rows = 5
        cols = 3
        data = full_data[:rows, :cols]
        with clib.Session() as lib:
            with lib.virtualfile_from_matrix(data) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", f"{vfile} ->{outfile.name}")
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join([f"<{col.min():.0f}/{col.max():.0f}>" for col in data.T])
            expected = f"<matrix memory>: N = {rows}\t{bounds}\n"
            assert output == expected


def test_virtualfile_from_vectors_pandas(dtypes_pandas):
    """
    Pass vectors to a dataset using pandas.Series, checking both numpy and pyarrow
    dtypes.
    """
    size = 13

    for dtype in dtypes_pandas:
        data = pd.DataFrame(
            data={
                "x": np.arange(size),
                "y": np.arange(size, size * 2, 1),
                "z": np.arange(size * 2, size * 3, 1),
            },
            dtype=dtype,
        )
        with clib.Session() as lib:
            with lib.virtualfile_from_vectors(data.x, data.y, data.z) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", f"{vfile} ->{outfile.name}")
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join(
                [f"<{i.min():.0f}/{i.max():.0f}>" for i in (data.x, data.y, data.z)]
            )
            expected = f"<vector memory>: N = {size}\t{bounds}\n"
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
                lib.call_module("info", f"{vfile} ->{outfile.name}")
                output = outfile.read(keep_tabs=True)
        bounds = "\t".join([f"<{min(i):.0f}/{max(i):.0f}>" for i in (x, y, z)])
        expected = f"<vector memory>: N = {size}\t{bounds}\n"
        assert output == expected
