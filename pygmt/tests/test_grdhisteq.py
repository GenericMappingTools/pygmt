"""
Tests for grdhisteq.
"""
import os

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from pygmt import grdhisteq, load_dataarray
from pygmt.datasets import load_earth_relief
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[-5, 5, -5, 5])


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected grdhisteq grid result.
    """
    return xr.DataArray(
        data=[[4.0, 0.0, 8.0, 11.0], [13.0, 4.0, 8.0, 13.0], [15.0, 15.0, 15.0, 15.0]],
        coords=dict(lon=[-2.5, -1.5, -0.5, 0.5], lat=[2.5, 3.5, 4.5]),
        dims=["lat", "lon"],
    )


@pytest.fixture(scope="module", name="expected_df")
def fixture_df_result():
    """
    Load the expected grdhisteq table result.
    """
    return pd.DataFrame(
        data=np.array(
            [
                [-5.1050e03, -5.1050e03, 0.0000e00],
                [-5.1050e03, -5.1050e03, 1.0000e00],
                [-5.1050e03, -5.0695e03, 2.0000e00],
                [-5.0695e03, -5.0695e03, 3.0000e00],
                [-5.0695e03, -4.9960e03, 4.0000e00],
                [-4.9960e03, -4.9960e03, 5.0000e00],
                [-4.9960e03, -4.9960e03, 6.0000e00],
                [-4.9960e03, -4.9370e03, 7.0000e00],
                [-4.9370e03, -4.7620e03, 8.0000e00],
                [-4.7620e03, -4.7620e03, 9.0000e00],
                [-4.7620e03, -4.7080e03, 1.0000e01],
                [-4.7080e03, -4.7080e03, 1.1000e01],
                [-4.7080e03, -4.5990e03, 1.2000e01],
                [-4.5990e03, -4.1155e03, 1.3000e01],
                [-4.1155e03, -3.8975e03, 1.4000e01],
                [-3.8975e03, -1.6000e02, 1.5000e01],
            ]
        )
    ).astype({0: np.float64, 1: np.float64, 2: np.int64})


def test_grdhisteq_outgrid_file(grid, expected_grid):
    """
    Test the gaussian parameter of grdhisteq with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdhisteq.equalize_grid(
            grid=grid, quadratic=True, region=[-3, 1, 2, 5], outgrid=tmpfile.name
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


@pytest.mark.parametrize("outgrid", [True, None])
def test_grdhisteq_outgrid(grid, outgrid, expected_grid):
    """
    Test the quadratic and region parameters for grdhisteq with
    ``outgrid=True`` and ``outgrid=None``.
    """
    temp_grid = grdhisteq.equalize_grid(
        grid=grid, quadratic=True, region=[-3, 1, 2, 5], outgrid=outgrid
    )
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 1  # Pixel registration
    xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdhisteq_no_outgrid(grid, expected_df):
    """
    Test the quadratic and region parameters for grdhisteq with no ``outgrid``.
    """
    temp_df = grdhisteq.compute_bins(
        grid=grid, quadratic=True, region=[-3, 1, 2, 5], outfile=True
    )
    assert isinstance(temp_df, pd.DataFrame)
    pd.testing.assert_frame_equal(left=temp_df, right=expected_df)


def test_grdhisteq_outfile(grid, expected_df):
    """
    Test the quadratic and region parameters for grdhisteq with no ``outgrid``.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        result = grdhisteq.compute_bins(
            grid=grid, quadratic=True, region=[-3, 1, 2, 5], outfile=tmpfile.name
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)
        temp_df = pd.read_csv(tmpfile.name, sep="\t", header=None)
        pd.testing.assert_frame_equal(left=temp_df, right=expected_df)
