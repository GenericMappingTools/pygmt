"""
Test the vectors_to_arrays function in the clib.conversion module.
"""

import datetime
import importlib

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt.clib.conversion import vectors_to_arrays

_HAS_PYARROW = bool(importlib.util.find_spec("pyarrow"))


def _check_arrays(arrays):
    """
    A helper function to check the results of vectors_to_arrays.

    - Check if all arrays are C-contiguous
    - Check if all arrays are numpy arrays
    - Check if all arrays are 1-D
    """
    # Check if all arrays are C-contiguous
    assert all(i.flags.c_contiguous for i in arrays)
    # Check if all arrays are numpy arrays
    assert all(isinstance(i, np.ndarray) for i in arrays)
    # Check if all arrays are 1-D
    assert all(i.ndim == 1 for i in arrays)


@pytest.mark.parametrize(
    "vectors",
    [
        pytest.param([[1, 2], (3, 4), range(5, 7)], id="python_sequences"),
        pytest.param(
            [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])], id="numpy_arrays"
        ),
        pytest.param([[1, 2], np.array([3, 4]), range(5, 7)], id="mixed_sequences"),
    ],
)
def test_vectors_to_arrays(vectors):
    """
    Test the vectors_to_arrays function for various input types.
    """
    arrays = vectors_to_arrays(vectors)
    npt.assert_equal(arrays, [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])])
    _check_arrays(arrays)


def test_vectors_to_arrays_scalars():
    """
    Test that the vectors_to_arrays function can deal with 0-D scalars.
    """
    arrays = vectors_to_arrays([1, 2, 3.0])
    npt.assert_equal(arrays, [np.array([1]), np.array([2]), np.array([3.0])])
    _check_arrays(arrays)


def test_vectors_to_arrays_not_c_contiguous():
    """
    Test the vectors_to_arrays function with numpy arrays that are not C-contiguous.
    """
    data = np.array([[1, 2], [3, 4], [5, 6]])
    vectors = [data[:, 0], data[:, 1]]
    assert all(not i.flags.c_contiguous for i in vectors)
    arrays = vectors_to_arrays(vectors)
    _check_arrays(arrays)


@pytest.mark.skipif(not _HAS_PYARROW, reason="pyarrow is not installed.")
def test_vectors_to_arrays_pyarrow_datetime():
    """
    Test the vectors_to_arrays function with pyarrow arrays containing date32/date64
    types.
    """
    vectors = [
        pd.Series(
            data=[datetime.date(2020, 1, 1), datetime.date(2021, 12, 31)],
            dtype="date32[day][pyarrow]",
        ),
        pd.Series(
            data=[datetime.date(2022, 1, 1), datetime.date(2023, 12, 31)],
            dtype="date64[ms][pyarrow]",
        ),
    ]
    arrays = vectors_to_arrays(vectors)
    assert all(i.dtype.type == np.datetime64 for i in arrays)
    _check_arrays(arrays)
