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
    Make sure grd2xyz works as expected.
    """
    xyz_data = grd2xyz(grid=grid, output_type="numpy")
    assert xyz_data.shape == (112, 3)


def test_grd2xyz_format(grid):
    """
    Test that correct formats are returned.
    """
    lon = -50.5
    lat = -18.5
    orig_val = grid.sel(lon=lon, lat=lat).to_numpy()
    xyz_default = grd2xyz(grid=grid)
    xyz_val = xyz_default[(xyz_default["lon"] == lon) & (xyz_default["lat"] == lat)][
        "z"
    ].to_numpy()
    assert isinstance(xyz_default, pd.DataFrame)
    assert orig_val.size == 1
    assert xyz_val.size == 1
    np.testing.assert_allclose(orig_val, xyz_val)
    xyz_array = grd2xyz(grid=grid, output_type="numpy")
    assert isinstance(xyz_array, np.ndarray)
    xyz_df = grd2xyz(grid=grid, output_type="pandas", outcols=None)
    assert isinstance(xyz_df, pd.DataFrame)
    assert list(xyz_df.columns) == ["lon", "lat", "z"]


def test_grd2xyz_pandas_output_with_o(grid):
    """
    Test that grd2xyz fails when outcols is set and output_type is set to 'pandas'.
    """
    with pytest.raises(GMTInvalidInput):
        grd2xyz(grid=grid, output_type="pandas", outcols="2")
