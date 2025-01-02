"""
Test the Session.virtualfile_in method.
"""

from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from packaging.version import Version
from pygmt import clib
from pygmt.clib import __gmt_version__
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, data_kind

POINTS_DATA = Path(__file__).parent / "data" / "points.txt"


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the point data from the test file.
    """
    return np.loadtxt(POINTS_DATA)


@pytest.mark.benchmark
@pytest.mark.parametrize(
    ("array_func", "kind"),
    [(np.array, "matrix"), (pd.DataFrame, "vector"), (xr.Dataset, "vector")],
)
def test_virtualfile_in_required_z_matrix(array_func, kind):
    """
    Test that function works when third z column in a matrix is needed and provided.
    """
    shape = (5, 3)
    dataframe = pd.DataFrame(
        data=np.arange(shape[0] * shape[1]).reshape(shape), columns=["x", "y", "z"]
    )
    data = array_func(dataframe)
    with clib.Session() as lib:
        with lib.virtualfile_in(
            data=data, required_z=True, check_kind="vector"
        ) as vfile:
            with GMTTempFile() as outfile:
                lib.call_module("info", [vfile, f"->{outfile.name}"])
                output = outfile.read(keep_tabs=True)
        bounds = "\t".join(
            [
                f"<{i.min():.0f}/{i.max():.0f}>"
                for i in (dataframe.x, dataframe.y, dataframe.z)
            ]
        )
        expected = f"<{kind} memory>: N = {shape[0]}\t{bounds}\n"
        assert output == expected


def test_virtualfile_in_required_z_matrix_missing():
    """
    Test that function fails when third z column in a matrix is needed but not provided.
    """
    data = np.ones((5, 2))
    with clib.Session() as lib:
        with pytest.raises(GMTInvalidInput):
            with lib.virtualfile_in(data=data, required_z=True, check_kind="vector"):
                pass


def test_virtualfile_in_fail_non_valid_data(data):
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
                lib.virtualfile_in(x=variable[0], y=variable[1])

    # Test all combinations where at least one data variable
    # is not given in the x, y, z case:
    for variable in product([None, data[:, 0]], repeat=3):
        # Filter one valid configuration:
        if not any(item is None for item in variable):
            continue
        with clib.Session() as lib:
            with pytest.raises(GMTInvalidInput):
                lib.virtualfile_in(
                    x=variable[0], y=variable[1], z=variable[2], required_z=True
                )

    # Should also fail if given too much data
    with clib.Session() as lib:
        with pytest.raises(GMTInvalidInput):
            lib.virtualfile_in(
                x=data[:, 0],
                y=data[:, 1],
                z=data[:, 2],
                data=data,
            )


# TODO(GMT>6.5.0): Remove the xfail marker for GMT<=6.5.0.
@pytest.mark.xfail(
    condition=Version(__gmt_version__) <= Version("6.5.0"),
    reason="Upstream bug fixed in https://github.com/GenericMappingTools/gmt/pull/8600",
)
def test_virtualfile_in_matrix_string_dtype():
    """
    Pass a string dtype matrix should work and the matrix should be passed via a series
    of vectors.
    """
    data = np.array([["11:30W", "30:30S"], ["12:30W", "30:00S"]])
    assert data_kind(data) == "matrix"  # data is recognized as "matrix" kind
    assert data.dtype.type == np.str_
    assert data.dtype.kind not in "iuf"  # dtype is not in numeric dtypes

    with clib.Session() as lib:
        with lib.virtualfile_in(data=data) as vintbl:
            with GMTTempFile() as outfile:
                lib.call_module("info", [vintbl, "-C", f"->{outfile.name}"])
                output = outfile.read(keep_tabs=False)
                assert output == "347.5 348.5 -30.5 -30\n"
                # Should check that lib.virtualfile_from_vectors is called once,
                # not lib.virtualfile_from_matrix, but it's technically complicated.


# TODO(PyGMT>=0.16.0): Remove this test in PyGMT v0.16.0 in which the old usage of
# virtualfile_from_data is removed.
def test_virtualfile_from_data():
    """
    Test the backwards compatibility of the virtualfile_from_data method.

    This test is the same as test_virtualfile_in_required_z_matrix, but using the
    deprecated method.
    """
    shape = (5, 3)
    dataframe = pd.DataFrame(
        data=np.arange(shape[0] * shape[1]).reshape(shape), columns=["x", "y", "z"]
    )
    data = np.array(dataframe)
    with clib.Session() as lib:
        with pytest.warns(FutureWarning, match="virtualfile_from_data"):
            with lib.virtualfile_from_data(
                data=data, required_z=True, check_kind="vector"
            ) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", [vfile, f"->{outfile.name}"])
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join(
                [
                    f"<{i.min():.0f}/{i.max():.0f}>"
                    for i in (dataframe.x, dataframe.y, dataframe.z)
                ]
            )
            expected = f"<matrix memory>: N = {shape[0]}\t{bounds}\n"
            assert output == expected
