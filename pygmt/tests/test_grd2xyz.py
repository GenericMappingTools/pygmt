"""
Tests for grd2xyz.
"""
import os

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from pygmt import grd2xyz
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[-1, 1, -1, 1])


def test_grd2xyz(grid):
    """
    Make sure grd2xyz works as expected.
    """
    xyz_data = grd2xyz(grid=grid, output_type="numpy")
    assert xyz_data.shape == (4, 3)


def test_grd2xyz_format(grid):
    """
    Test that correct formats are returned.
    """
    xyz_default = grd2xyz(grid=grid)
    assert isinstance(xyz_default, pd.DataFrame)
    print(type(list(xyz_default.columns)))
    assert list(xyz_default.columns) == ["x", "y", "z"]
    xyz_array = grd2xyz(grid=grid, output_type="numpy")
    assert isinstance(xyz_array, np.ndarray)
    xyz_df = grd2xyz(grid=grid, output_type="pandas")
    assert isinstance(xyz_df, pd.DataFrame)
    assert list(xyz_df.columns) == ["x", "y", "z"]


def test_grd2xyz_file_output(grid):
    """
    Test that grd2xyz returns a file output when it is specified.
    """
    with GMTTempFile(suffix=".xyz") as tmpfile:
        result = grd2xyz(grid=grid, outfile=tmpfile.name, output_type="file")
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outfile exists


def test_grd2xyz_invalid_format(grid):
    """
    Test that grd2xyz fails with incorrect format.
    """
    with pytest.raises(GMTInvalidInput):
        grd2xyz(grid=grid, output_type=1)


def test_grd2xyz_no_outfile(grid):
    """
    Test that grd2xyz fails when a string output is set with no outfile.
    """
    with pytest.raises(GMTInvalidInput):
        grd2xyz(grid=grid, output_type="file")
