"""
Test pygmt.grdclip.
"""

from pathlib import Path

import numpy as np
import numpy.testing as npt
import pytest
import xarray as xr
from pygmt import grdclip
from pygmt.datasets import load_earth_mask
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected grdclip grid result.
    """
    return xr.DataArray(
        data=[
            [1000.0, 570.5, -1000.0, -1000.0],
            [1000.0, 1000.0, 571.5, 638.5],
            [555.5, 556.0, 580.0, 1000.0],
        ],
        coords={"lon": [-52.5, -51.5, -50.5, -49.5], "lat": [-18.5, -17.5, -16.5]},
        dims=["lat", "lon"],
    )


def test_grdclip_outgrid(grid, expected_grid):
    """
    Test the below and above parameters for grdclip and creates a test outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdclip(
            grid=grid,
            outgrid=tmpfile.name,
            below=[550, -1000],
            above=[700, 1000],
            region=[-53, -49, -19, -16],
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
        temp_grid = xr.load_dataarray(tmpfile.name, engine="gmt", raster_kind="grid")
        assert temp_grid.dims == ("lat", "lon")
        assert temp_grid.gmt.gtype is GridType.GEOGRAPHIC
        assert temp_grid.gmt.registration is GridRegistration.PIXEL
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


@pytest.mark.benchmark
def test_grdclip_no_outgrid(grid, expected_grid):
    """
    Test the below and above parameters for grdclip with no set outgrid.
    """
    temp_grid = grdclip(
        grid=grid, below=[550, -1000], above=[700, 1000], region=[-53, -49, -19, -16]
    )
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype is GridType.GEOGRAPHIC
    assert temp_grid.gmt.registration is GridRegistration.PIXEL
    xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdclip_replace():
    """
    Test the replace parameter for grdclip.
    """
    grid = load_earth_mask(region=[0, 10, 0, 10])
    npt.assert_array_equal(np.unique(grid), [0, 1])  # Only have 0 and 1
    grid = grdclip(grid=grid, replace=[0, 2])  # Replace 0 with 2
    npt.assert_array_equal(np.unique(grid), [1, 2])


def test_grdclip_between_repeated():
    """
    Test passing a 2-D sequence to the between parameter for grdclip.
    """
    grid = load_static_earth_relief()
    # Replace values in the range 0-250 with 0, 250-500 with 1, 500-750 with 2, and
    # 750-1000 with 3
    result = grdclip(
        grid,
        between=[[0, 250, 0], [250, 500, 1], [500, 750, 2], [750, 1000, 3]],
    )
    # Result should have 4 unique values.
    npt.assert_array_equal(np.unique(result.data), [0, 1, 2, 3])


def test_grdclip_missing_required_parameter(grid):
    """
    Test that grdclip raises a ValueError if the required parameter is missing.
    """
    with pytest.raises(GMTParameterError):
        grdclip(grid=grid)
