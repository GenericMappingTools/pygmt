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

def test_grdvolume_format(grid):
    """
    Test that correct formats are returned.
    """
    grdvolume_default = grdvolume(grid=grid)
    assert isinstance(grdvolume_default, pd.DataFrame)
    grdvolume_array = grdvolume(grid=grid, output_type="numpy")
    assert isinstance(grdvolume_array, np.ndarray)
    grdvolume_df = grdvolume(grid=grid, output_type="pandas")
    assert isinstance(grdvolume_df, pd.DataFrame)


def test_grdvolume_invalid_format(grid):
    """
    Test that grdvolume fails with incorrect output_type argument.
    """
    with pytest.raises(GMTInvalidInput):
        grdvolume(grid=grid, output_type=1)
