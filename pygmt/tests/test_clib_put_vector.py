"""
Test the functions that put vector data into GMT.
"""
import itertools
from datetime import datetime

import numpy as np
import numpy.testing as npt
import pytest
from pygmt import clib
from pygmt.exceptions import GMTCLibError, GMTInvalidInput
from pygmt.helpers import GMTTempFile


def test_put_vector():
    """
    Check that assigning a numpy array to a dataset works.
    """
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


def test_put_vector_mixed_dtypes():
    """
    Passing a numpy array of mixed dtypes to a dataset.

    See https://github.com/GenericMappingTools/pygmt/issues/255
    """
    dtypes = "float32 float64 int32 int64 uint32 uint64".split()
    for dtypex, dtypey in itertools.permutations(dtypes, r=2):
        with clib.Session() as lib:
            dataset = lib.create_data(
                family="GMT_IS_DATASET|GMT_VIA_VECTOR",
                geometry="GMT_IS_POINT",
                mode="GMT_CONTAINER_ONLY",
                dim=[2, 5, 1, 0],  # columns, rows, layers, dtype
            )
            x = np.array([1, 2, 3, 4, 5], dtype=dtypex)
            y = np.array([6, 7, 8, 9, 10], dtype=dtypey)
            lib.put_vector(dataset, column=lib["GMT_X"], vector=x)
            lib.put_vector(dataset, column=lib["GMT_Y"], vector=y)
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
                newx, newy = tmp_file.loadtxt(
                    unpack=True, dtype=[("x", dtypex), ("y", dtypey)]
                )
                assert x.dtype == newx.dtype
                assert y.dtype == newy.dtype
                npt.assert_allclose(newx, x)
                npt.assert_allclose(newy, y)


def test_put_vector_string_dtype():
    """
    Passing string type vectors to a dataset.
    """
    # input string vectors: numbers, longitudes, latitudes, and datetimes
    vectors = np.array(
        [
            ["10", "20.0", "-30.0", "3.5e1"],
            ["10W", "30.50E", "30:30W", "40:30:30.500E"],
            ["10N", "30.50S", "30:30N", "40:30:30.500S"],
            ["2021-02-03", "2021-02-03T04", "2021-02-03T04:05:06.700", "T04:50:06.700"],
        ]
    )
    # output vectors in double or string type
    # Notes:
    # 1. longitudes and latitudes are stored in double in GMT
    # 2. The default output format for datetime is YYYY-mm-ddTHH:MM:SS
    expected_vectors = [
        [10.0, 20.0, -30.0, 35],
        [-10, 30.5, -30.5, 40.508472],
        [10, -30.50, 30.5, -40.508472],
        [
            "2021-02-03T00:00:00",
            "2021-02-03T04:00:00",
            "2021-02-03T04:05:06",
            f"{datetime.utcnow().strftime('%Y-%m-%d')}T04:50:06",
        ],
    ]

    # loop over all possible combinations of input types
    for i, j in itertools.combinations_with_replacement(range(4), r=2):
        with clib.Session() as lib:
            dataset = lib.create_data(
                family="GMT_IS_DATASET|GMT_VIA_VECTOR",
                geometry="GMT_IS_POINT",
                mode="GMT_CONTAINER_ONLY",
                dim=[2, 4, 1, 0],  # columns, rows, layers, dtype
            )
            lib.put_vector(dataset, column=lib["GMT_X"], vector=vectors[i])
            lib.put_vector(dataset, column=lib["GMT_Y"], vector=vectors[j])
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
                # Load the data
                output = np.genfromtxt(
                    tmp_file.name, dtype=None, names=("x", "y"), encoding=None
                )
                # check that the output is correct
                # Use npt.assert_allclose for numeric arrays
                # and npt.assert_array_equal for string arrays
                if i != 3:
                    npt.assert_allclose(output["x"], expected_vectors[i])
                else:
                    npt.assert_array_equal(output["x"], expected_vectors[i])
                if j != 3:
                    npt.assert_allclose(output["y"], expected_vectors[j])
                else:
                    npt.assert_array_equal(output["y"], expected_vectors[j])


def test_put_vector_invalid_dtype():
    """
    Check that it fails with an exception for invalid data types.
    """
    with clib.Session() as lib:
        dataset = lib.create_data(
            family="GMT_IS_DATASET|GMT_VIA_VECTOR",
            geometry="GMT_IS_POINT",
            mode="GMT_CONTAINER_ONLY",
            dim=[2, 3, 1, 0],  # columns, rows, layers, dtype
        )
        data = np.array([37, 12, 556], dtype="object")
        with pytest.raises(GMTInvalidInput):
            lib.put_vector(dataset, column=1, vector=data)


def test_put_vector_wrong_column():
    """
    Check that it fails with an exception when giving an invalid column.
    """
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
    """
    Check that it fails with an exception for multidimensional arrays.
    """
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
