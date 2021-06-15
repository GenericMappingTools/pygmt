"""
Tests for grdvolume.
"""
import numpy as np
import pandas as pd
import pytest
from pygmt import grdvolume
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[-1, 1, -1, 1])


def test_grdvolume(grid):
    """
    Make sure grdvolume works as expected.
    """
    volume_data = grdvolume(grid=grid, data_format="s")
    assert volume_data.strip().split() == [
        "0",
        "49453592037.5",
        "-2.40882119642e+14",
        "-4870.87205839",
    ]


def test_grdvolume_format(grid):
    """
    Test that correct formats are returned.
    """
    grdvolume_array = grdvolume(grid=grid)
    assert isinstance(grdvolume_array, np.ndarray)
    grdvolume_df = grdvolume(grid=grid, data_format="d")
    assert isinstance(grdvolume_df, pd.DataFrame)
    grdvolume_string = grdvolume(grid=grid, data_format="s")
    assert isinstance(grdvolume_string, str)
