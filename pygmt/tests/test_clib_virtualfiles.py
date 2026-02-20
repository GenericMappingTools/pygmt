"""
Test the Session.open_virtualfile method.
"""

from pathlib import Path

import numpy as np
import pytest
from pygmt import clib
from pygmt.clib.session import DTYPES_NUMERIC
from pygmt.exceptions import GMTCLibError, GMTValueError
from pygmt.helpers import GMTTempFile
from pygmt.tests.test_clib import mock

POINTS_DATA = Path(__file__).parent / "data" / "points.txt"


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
    return [dtype for dtype in DTYPES_NUMERIC if dtype != np.timedelta64]


@pytest.mark.benchmark
def test_open_virtualfile(dtypes):
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
                dim=[shape[1], shape[0], 1, 0],  # ncolumns, nrows, nlayers, dtype
            )
            data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
            lib.put_matrix(dataset, matrix=data)
            # Add the dataset to a virtual file and pass it along to gmt info
            vfargs = (family, geometry, "GMT_IN", dataset)
            with lib.open_virtualfile(*vfargs) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", [vfile, f"->{outfile.name}"])
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join([f"<{col.min():.0f}/{col.max():.0f}>" for col in data.T])
            expected = f"<matrix memory>: N = {shape[0]}\t{bounds}\n"
            assert output == expected


def test_open_virtualfile_fails():
    """
    Check that opening and closing virtual files raises an exception for non- zero
    return codes.
    """
    vfargs = (
        "GMT_IS_DATASET|GMT_VIA_MATRIX",
        "GMT_IS_POINT",
        "GMT_IN",
        None,
    )

    # Mock Open_VirtualFile to test the status check when entering the context.
    # If the exception is raised, the code won't get to the closing of the
    # virtual file.
    with clib.Session() as lib, mock(lib, "GMT_Open_VirtualFile", returns=1):
        with pytest.raises(GMTCLibError):
            with lib.open_virtualfile(*vfargs):
                pass

    # Test the status check when closing the virtual file
    # Mock the opening to return 0 (success) so that we don't open a file that
    # we won't close later.
    with (
        clib.Session() as lib,
        mock(lib, "GMT_Open_VirtualFile", returns=0),
        mock(lib, "GMT_Close_VirtualFile", returns=1),
    ):
        with pytest.raises(GMTCLibError):
            with lib.open_virtualfile(*vfargs):
                pass


def test_open_virtualfile_bad_direction():
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
        with pytest.raises(GMTValueError):
            with lib.open_virtualfile(*vfargs):
                pass
