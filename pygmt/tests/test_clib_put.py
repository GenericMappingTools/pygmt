"""
Test the functions that put data into GMT.
"""
import numpy as np
import numpy.testing as npt
import pytest

from .test_clib import mock
from .. import clib
from ..exceptions import GMTCLibError, GMTInvalidInput
from ..helpers import GMTTempFile


def test_put_strings():
    "Check that assigning a numpy array of dtype str to a dataset works"
    with clib.Session() as lib:
        dataset = lib.create_data(
            family="GMT_IS_DATASET|GMT_VIA_VECTOR",
            geometry="GMT_IS_POINT",
            mode="GMT_CONTAINER_ONLY",
            dim=[1, 5, 1, 0],  # columns, rows, layers, dtype
        )
        s = np.array(["a", "b", "c", "d", "e"], dtype=np.str)
        lib.put_strings(dataset, column=lib["GMT_S"], strings=s)
        # Turns out wesn doesn't matter for Datasets
        wesn = [0] * 6
        # Save the data to a file to see if it's being accessed correctly
        with GMTTempFile() as tmp_file:
            lib.write_data(
                "GMT_IS_VECTOR",
                "GMT_IS_POINT",
                "GMT_WRITE_SET",
                wesn,
                tmp_file.name,
                dataset,
            )
            # Load the data and check that it's correct
            news = tmp_file.loadtxt(unpack=True, dtype=np.str)
            npt.assert_allclose(news, s)


def test_put_vector():
    "Check that assigning a numpy array to a dataset works"
    dtypes = "float32 float64 int32 int64 uint32 uint64".split()
    for dtype in dtypes:
        with clib.Session() as lib:
            dataset = lib.create_data(
                family="GMT_IS_DATASET|GMT_VIA_VECTOR",
                geometry="GMT_IS_POINT",
                mode="GMT_CONTAINER_ONLY",
                dim=[3, 5, 1, 0],  # columns, rows, layers, dtype
            )
            x = np.array([1, 2, 3, 4, 5], dtype=dtype)
            y = np.array([6, 7, 8, 9, 10], dtype=dtype)
            z = np.array([11, 12, 13, 14, 15], dtype=dtype)
            lib.put_vector(dataset, column=lib["GMT_X"], vector=x)
            lib.put_vector(dataset, column=lib["GMT_Y"], vector=y)
            lib.put_vector(dataset, column=lib["GMT_Z"], vector=z)
            # Turns out wesn doesn't matter for Datasets
            wesn = [0] * 6
            # Save the data to a file to see if it's being accessed correctly
            with GMTTempFile() as tmp_file:
                lib.write_data(
                    "GMT_IS_VECTOR",
                    "GMT_IS_POINT",
                    "GMT_WRITE_SET",
                    wesn,
                    tmp_file.name,
                    dataset,
                )
                # Load the data and check that it's correct
                newx, newy, newz = tmp_file.loadtxt(unpack=True, dtype=dtype)
                npt.assert_allclose(newx, x)
                npt.assert_allclose(newy, y)
                npt.assert_allclose(newz, z)


def test_put_vector_invalid_dtype():
    "Check that it fails with an exception for invalid data types"
    with clib.Session() as lib:
        dataset = lib.create_data(
            family="GMT_IS_DATASET|GMT_VIA_VECTOR",
            geometry="GMT_IS_POINT",
            mode="GMT_CONTAINER_ONLY",
            dim=[2, 3, 1, 0],  # columns, rows, layers, dtype
        )
        data = np.array([37, 12, 556], dtype="complex128")
        with pytest.raises(GMTInvalidInput):
            lib.put_vector(dataset, column=1, vector=data)


def test_put_vector_wrong_column():
    "Check that it fails with an exception when giving an invalid column"
    with clib.Session() as lib:
        dataset = lib.create_data(
            family="GMT_IS_DATASET|GMT_VIA_VECTOR",
            geometry="GMT_IS_POINT",
            mode="GMT_CONTAINER_ONLY",
            dim=[1, 3, 1, 0],  # columns, rows, layers, dtype
        )
        data = np.array([37, 12, 556], dtype="float32")
        with pytest.raises(GMTCLibError):
            lib.put_vector(dataset, column=1, vector=data)


def test_put_vector_2d_fails():
    "Check that it fails with an exception for multidimensional arrays"
    with clib.Session() as lib:
        dataset = lib.create_data(
            family="GMT_IS_DATASET|GMT_VIA_VECTOR",
            geometry="GMT_IS_POINT",
            mode="GMT_CONTAINER_ONLY",
            dim=[1, 6, 1, 0],  # columns, rows, layers, dtype
        )
        data = np.array([[37, 12, 556], [37, 12, 556]], dtype="int32")
        with pytest.raises(GMTInvalidInput):
            lib.put_vector(dataset, column=0, vector=data)


def test_put_matrix():
    "Check that assigning a numpy 2d array to a dataset works"
    dtypes = "float32 float64 int32 int64 uint32 uint64".split()
    shape = (3, 4)
    for dtype in dtypes:
        with clib.Session() as lib:
            dataset = lib.create_data(
                family="GMT_IS_DATASET|GMT_VIA_MATRIX",
                geometry="GMT_IS_POINT",
                mode="GMT_CONTAINER_ONLY",
                dim=[shape[1], shape[0], 1, 0],  # columns, rows, layers, dtype
            )
            data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
            lib.put_matrix(dataset, matrix=data)
            # wesn doesn't matter for Datasets
            wesn = [0] * 6
            # Save the data to a file to see if it's being accessed correctly
            with GMTTempFile() as tmp_file:
                lib.write_data(
                    "GMT_IS_MATRIX",
                    "GMT_IS_POINT",
                    "GMT_WRITE_SET",
                    wesn,
                    tmp_file.name,
                    dataset,
                )
                # Load the data and check that it's correct
                newdata = tmp_file.loadtxt(dtype=dtype)
                npt.assert_allclose(newdata, data)


def test_put_matrix_fails():
    "Check that put_matrix raises an exception if return code is not zero"
    # It's hard to make put_matrix fail on the C API level because of all the
    # checks on input arguments. Mock the C API function just to make sure it
    # works.
    with clib.Session() as lib:
        with mock(lib, "GMT_Put_Matrix", returns=1):
            with pytest.raises(GMTCLibError):
                lib.put_matrix(dataset=None, matrix=np.empty((10, 2)), pad=0)


def test_put_matrix_grid():
    "Check that assigning a numpy 2d array to a grid works"
    dtypes = "float32 float64 int32 int64 uint32 uint64".split()
    wesn = [10, 15, 30, 40, 0, 0]
    inc = [1, 1]
    shape = ((wesn[3] - wesn[2]) // inc[1] + 1, (wesn[1] - wesn[0]) // inc[0] + 1)
    for dtype in dtypes:
        with clib.Session() as lib:
            grid = lib.create_data(
                family="GMT_IS_GRID|GMT_VIA_MATRIX",
                geometry="GMT_IS_SURFACE",
                mode="GMT_CONTAINER_ONLY",
                ranges=wesn[:4],
                inc=inc,
                registration="GMT_GRID_NODE_REG",
            )
            data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
            lib.put_matrix(grid, matrix=data)
            # Save the data to a file to see if it's being accessed correctly
            with GMTTempFile() as tmp_file:
                lib.write_data(
                    "GMT_IS_MATRIX",
                    "GMT_IS_SURFACE",
                    "GMT_CONTAINER_AND_DATA",
                    wesn,
                    tmp_file.name,
                    grid,
                )
                # Load the data and check that it's correct
                newdata = tmp_file.loadtxt(dtype=dtype)
                npt.assert_allclose(newdata, data)
