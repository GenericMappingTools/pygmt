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
    xyz_data = grd2xyz(grid=grid, output_type="s")
    assert xyz_data.strip().split("\n") == [
        "-0.5 0.5 -4967",
        "0.5 0.5 -4852",
        "-0.5 -0.5 -4917",
        "0.5 -0.5 -4747.5",
    ]


def test_grd2xyz_format(grid):
    """
    Test that correct formats are returned.
    """
    xyz_array = grd2xyz(grid=grid)
    assert isinstance(xyz_array, np.ndarray)
    xyz_df = grd2xyz(grid=grid, output_type="d")
    assert isinstance(xyz_df, pd.DataFrame)
    xyz_string = grd2xyz(grid=grid, output_type="s")
    assert isinstance(xyz_string, str)


def test_grd2xyz_invalid_format(grid):
    """
    Test that grd2xyz fails with incorrect format.
    """
    with pytest.raises(GMTInvalidInput):
        grd2xyz(grid=grid, output_type=1)
