"""
Test pygmt.grd2xyz.
"""

import numpy as np
import pandas as pd
import pytest
from pygmt import grd2xyz
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file.
    """
    return load_static_earth_relief()


@pytest.mark.benchmark
def test_grd2xyz(grid):
    """
    Test the basic functionality of grd2xyz.
    """
    xyz_df = grd2xyz(grid=grid)
    assert isinstance(xyz_df, pd.DataFrame)
    assert list(xyz_df.columns) == ["lon", "lat", "z"]
    assert xyz_df.shape == (112, 3)

    lon, lat = -50.5, -18.5
    orig_val = grid.sel(lon=lon, lat=lat).to_numpy()
    xyz_val = xyz_df[(xyz_df["lon"] == lon) & (xyz_df["lat"] == lat)]["z"].to_numpy()
    np.testing.assert_allclose(orig_val, xyz_val)


def test_grd2xyz_pandas_output_with_o(grid):
    """
    Test that grd2xyz fails when outcols is set and output_type is set to 'pandas'.
    """
    with pytest.raises(GMTInvalidInput):
        grd2xyz(grid=grid, output_type="pandas", outcols="2")
