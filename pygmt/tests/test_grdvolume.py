"""
Tests for grdvolume.
"""
from pathlib import Path

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import grdvolume
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    Set the data region for the tests.
    """
    return [-53, -50, -22, -20]


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the expected grdvolume data result as a numpy array.
    """
    data = np.array(
        [
            [2.00000000e02, 2.30079975e10, 3.92142453e12, 1.70437454e02],
            [2.50000000e02, 2.30079975e10, 2.77102465e12, 1.20437454e02],
            [3.00000000e02, 2.30079975e10, 1.62062477e12, 7.04374542e01],
            [3.50000000e02, 1.76916116e10, 4.53991397e11, 2.56613930e01],
            [4.00000000e02, 2.81602292e09, 2.34764859e10, 8.33675242e00],
        ]
    )
    return data


def test_grdvolume_format(grid, region):
    """
    Test that correct formats are returned.
    """
    grdvolume_default = grdvolume(grid=grid, region=region)
    assert isinstance(grdvolume_default, pd.DataFrame)
    grdvolume_array = grdvolume(grid=grid, output_type="numpy", region=region)
    assert isinstance(grdvolume_array, np.ndarray)
    grdvolume_df = grdvolume(grid=grid, output_type="pandas", region=region)
    assert isinstance(grdvolume_df, pd.DataFrame)


def test_grdvolume_invalid_format(grid):
    """
    Test that grdvolume fails with incorrect output_type argument.
    """
    with pytest.raises(GMTInvalidInput):
        grdvolume(grid=grid, output_type=1)


def test_grdvolume_no_outfile(grid):
    """
    Test that grdvolume fails when output_type set to 'file' but no outfile is
    specified.
    """
    with pytest.raises(GMTInvalidInput):
        grdvolume(grid=grid, output_type="file")


def test_grdvolume_no_outgrid(grid, data, region):
    """
    Test the expected output of grdvolume with no output file set.
    """
    test_output = grdvolume(
        grid=grid, contour=[200, 400, 50], output_type="numpy", region=region
    )
    npt.assert_allclose(test_output, data)


def test_grdvolume_outgrid(grid, region):
    """
    Test the expected output of grdvolume with an output file set.
    """
    with GMTTempFile(suffix=".csv") as tmpfile:
        result = grdvolume(
            grid=grid,
            contour=[200, 400, 50],
            output_type="file",
            outfile=tmpfile.name,
            region=region,
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outfile exists
