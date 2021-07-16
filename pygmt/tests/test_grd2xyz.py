"""
Tests for grd2xyz.
"""
import numpy as np
import pandas as pd
import pytest
from pygmt import grd2xyz
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput


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
    xyz_data = grd2xyz(grid=grid, output_type="a")
    assert xyz_data.shape == (4, 3)


def test_grd2xyz_format(grid):
    """
    Test that correct formats are returned.
    """
    xyz_default = grd2xyz(grid=grid)
    assert isinstance(xyz_default, pd.DataFrame)
    xyz_array = grd2xyz(grid=grid, output_type="a")
    assert isinstance(xyz_array, np.ndarray)
    xyz_df = grd2xyz(grid=grid, output_type="d")
    assert isinstance(xyz_df, pd.DataFrame)


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
        grd2xyz(grid=grid, output_type="s")
