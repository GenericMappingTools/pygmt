"""
Test the Session.virtualfile_from_matrix method.
"""

import numpy as np
import pytest
from pygmt import clib
from pygmt.clib.session import DTYPES_NUMERIC
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="dtypes")
def fixture_dtypes():
    """
    List of supported numpy dtypes.
    """
    return [dtype for dtype in DTYPES_NUMERIC if dtype != np.timedelta64]


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
                    lib.call_module("info", [vfile, f"->{outfile.name}"])
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
                    lib.call_module("info", [vfile, f"->{outfile.name}"])
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join([f"<{col.min():.0f}/{col.max():.0f}>" for col in data.T])
            expected = f"<matrix memory>: N = {rows}\t{bounds}\n"
            assert output == expected
