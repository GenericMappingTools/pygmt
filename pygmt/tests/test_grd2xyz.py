"""
Tests for grd2xyz.
"""
import os

import numpy as np
import pandas as pd
import pytest
from pygmt import grd2xyz
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[-1, 1, 3, 5])


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
    lon = -0.5
    lat = 3.5
    orig_val = grid.sel(lon=lon, lat=lat).to_numpy()
    xyz_default = grd2xyz(grid=grid)
    xyz_val = xyz_default[(xyz_default["lon"] == lon) & (xyz_default["lat"] == lat)][
        "elevation"
    ].to_numpy()
    assert isinstance(xyz_default, pd.DataFrame)
    assert orig_val.size == 1
    assert xyz_val.size == 1
    np.testing.assert_allclose(orig_val, xyz_val)
    xyz_array = grd2xyz(grid=grid, output_type="numpy")
    assert isinstance(xyz_array, np.ndarray)
    xyz_df = grd2xyz(grid=grid, output_type="pandas")
    assert isinstance(xyz_df, pd.DataFrame)
    assert list(xyz_df.columns) == ["lon", "lat", "elevation"]


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


def test_grd2xyz_outfile_incorrect_output_type(grid):
    """
    Test that grd2xyz raises a warning when an outfile filename is set but the
    output_type is not set to 'file'.
    """
    with pytest.warns(RuntimeWarning):
        with GMTTempFile(suffix=".xyz") as tmpfile:
            result = grd2xyz(grid=grid, outfile=tmpfile.name, output_type="numpy")
            assert result is None  # return value is None
            assert os.path.exists(path=tmpfile.name)  # check that outfile exists


def test_grd2xyz_pandas_output_with_o(grid):
    """
    Test that grd2xyz fails when outcols is set and output_type is set to
    'pandas'.
    """
    with pytest.raises(GMTInvalidInput):
        grd2xyz(grid=grid, output_type="pandas", outcols="2")
