"""
Test the functions that put string data into GMT.
"""
import numpy as np
import numpy.testing as npt
import pytest
from packaging.version import Version
from pygmt import clib
from pygmt.exceptions import GMTCLibError
from pygmt.helpers import GMTTempFile

with clib.Session() as _lib:
    gmt_version = Version(_lib.info["version"])


def test_put_strings():
    """
    Check that assigning a numpy array of dtype str to a dataset works.
    """
    with clib.Session() as lib:
        dataset = lib.create_data(
            family="GMT_IS_DATASET|GMT_VIA_VECTOR",
            geometry="GMT_IS_POINT",
            mode="GMT_CONTAINER_ONLY",
            dim=[2, 5, 1, 0],  # columns, rows, layers, dtype
        )
        x = np.array([1, 2, 3, 4, 5], dtype=np.int32)
        y = np.array([6, 7, 8, 9, 10], dtype=np.int32)
        strings = np.array(["a", "bc", "defg", "hijklmn", "opqrst"], dtype=str)
        lib.put_vector(dataset, column=lib["GMT_X"], vector=x)
        lib.put_vector(dataset, column=lib["GMT_Y"], vector=y)
        lib.put_strings(
            dataset, family="GMT_IS_VECTOR|GMT_IS_DUPLICATE", strings=strings
        )
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
            newx, newy, newstrings = tmp_file.loadtxt(
                unpack=True, dtype=[("x", np.int32), ("y", np.int32), ("text", "<U7")]
            )
            npt.assert_array_equal(newx, x)
            npt.assert_array_equal(newy, y)
            npt.assert_array_equal(newstrings, strings)


def test_put_strings_fails():
    """
    Check that put_strings raises an exception if return code is not zero.
    """
    with clib.Session() as lib:
        with pytest.raises(GMTCLibError):
            lib.put_strings(
                dataset=None,
                family="GMT_IS_VECTOR|GMT_IS_DUPLICATE",
                strings=np.empty(shape=(3,), dtype=str),
            )
