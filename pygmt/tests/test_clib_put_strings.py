"""
Test the functions that put string data into GMT.
"""
import numpy as np
import numpy.testing as npt


from .. import clib
from ..helpers import GMTTempFile


def test_put_strings():
    "Check that assigning a numpy array of dtype str to a dataset works"
    with clib.Session() as lib:
        dataset = lib.create_data(
            family="GMT_IS_DATASET|GMT_VIA_VECTOR",
            geometry="GMT_IS_POINT",
            mode="GMT_CONTAINER_ONLY",
            dim=[2, 5, 1, 0],  # columns, rows, layers, dtype
        )
        x = np.array([1, 2, 3, 4, 5], dtype=np.int32)
        y = np.array([6, 7, 8, 9, 10], dtype=np.int32)
        strings = np.array(["a", "b", "c", "d", "e"], dtype=np.str)
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
            print(tmp_file.read())
            # Load the data and check that it's correct
            newstrings = tmp_file.loadtxt(unpack=True, dtype=np.str)
            print(newstrings)
            # npt.assert_string_equal(news, s)
            npt.assert_allclose(newstrings, strings)
