"""
Test pygmt.grdfill.
"""

from pathlib import Path

import numpy as np
import numpy.testing as npt
import pytest
import xarray as xr
from pygmt import grdfill
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file and set value(s) to NaN and
    inf.
    """
    grid = load_static_earth_relief()
    grid[3:6, 3:5] = np.nan
    grid[6:8, 2:4] = np.inf
    return grid


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected grdfill grid result.
    """
    return xr.DataArray(
        data=[
            [347.5, 344.5, 386.0, 640.5, 617.0, 579.0, 646.5, 671.0],
            [383.0, 284.5, 344.5, 394.0, 491.0, 556.5, 578.5, 618.5],
            [373.0, 367.5, 349.0, 352.5, 419.5, 428.0, 570.0, 667.5],
            [557.0, 435.0, 385.5, 20.0, 20.0, 496.0, 519.5, 833.5],
            [561.5, 539.0, 446.5, 20.0, 20.0, 553.0, 726.5, 981.0],
            [310.0, 521.5, 757.0, 20.0, 20.0, 524.0, 686.5, 794.0],
            [521.5, 682.5, np.inf, np.inf, 571.5, 638.5, 739.5, 881.5],
            [308.0, 595.5, np.inf, np.inf, 580.0, 770.0, 927.0, 920.0],
            [601.0, 526.5, 535.0, 299.0, 398.5, 645.0, 797.5, 964.0],
            [494.5, 488.5, 357.0, 254.5, 286.0, 484.5, 653.5, 930.0],
            [450.5, 395.5, 366.0, 248.0, 250.0, 354.5, 550.0, 797.5],
            [345.5, 320.0, 335.0, 292.0, 207.5, 247.0, 325.0, 346.5],
            [349.0, 313.0, 325.5, 247.0, 191.0, 225.0, 260.0, 452.5],
            [347.5, 331.5, 309.0, 282.0, 190.0, 208.0, 299.5, 348.0],
        ],
        coords={
            "lon": np.arange(-54.5, -46.5, 1),
            "lat": np.arange(-23.5, -9.5, 1),
        },
        dims=["lat", "lon"],
    )


@pytest.mark.benchmark
def test_grdfill_dataarray_out(grid, expected_grid):
    """
    Test grdfill with a DataArray output.
    """
    result = grdfill(grid=grid, constant_fill=20)
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype is GridType.GEOGRAPHIC
    assert result.gmt.registration is GridRegistration.PIXEL
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdfill_asymmetric_pad(grid, expected_grid):
    """
    Test grdfill using a region that includes the edge of the grid.

    Regression test for https://github.com/GenericMappingTools/pygmt/issues/1745.
    """
    result = grdfill(grid=grid, constant_fill=20, region=[-55, -50, -24, -16])
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype is GridType.GEOGRAPHIC
    assert result.gmt.registration is GridRegistration.PIXEL
    # check information of the output grid
    xr.testing.assert_allclose(
        a=result, b=expected_grid.sel(lon=slice(-55, -50), lat=slice(-24, -16))
    )


def test_grdfill_file_out(grid, expected_grid):
    """
    Test grdfill with an outgrid set.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdfill(grid=grid, constant_fill=20, outgrid=tmpfile.name)
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outfile exists
        temp_grid = xr.load_dataarray(tmpfile.name, engine="gmt", raster_kind="grid")
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdfill_grid_fill_dataarray(grid):
    """
    Test grdfill with a DataArray input.
    """
    bggrid = xr.DataArray(
        np.arange(grid.size).reshape(grid.shape),
        dims=grid.dims,
        coords={"lon": grid.lon, "lat": grid.lat},
    )
    result = grdfill(grid=grid, grid_fill=bggrid)
    assert not result.isnull().any()
    npt.assert_array_equal(result[3:6, 3:5], bggrid[3:6, 3:5])


def test_grdfill_hole(grid, expected_grid):
    """
    Test grdfill with a custom value (not NaN) as holes.
    """
    # Prepare for a grid with a node value of -99999 for holes.
    grid_no_nan = grdfill(grid=grid, constant_fill=-99999)
    assert not np.isnan(grid_no_nan).any()
    assert -99999 in grid_no_nan
    # Now fill them with a constant value of 20.
    result = grdfill(grid=grid_no_nan, constant_fill=20, hole=-99999)

    # Check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype is GridType.GEOGRAPHIC
    assert result.gmt.registration is GridRegistration.PIXEL
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdfill_inquire(grid):
    """
    Test grdfill with inquire mode.
    """
    bounds = grdfill(grid=grid, inquire=True)
    assert isinstance(bounds, np.ndarray)
    assert bounds.shape == (1, 4)
    npt.assert_allclose(bounds, [[-52.0, -50.0, -21.0, -18.0]])


def test_grdfill_required_args(grid):
    """
    Test that grdfill fails without filling parameters or 'inquire'.
    """
    with pytest.raises(GMTParameterError):
        grdfill(grid=grid)


def test_grdfill_inquire_and_fill(grid):
    """
    Test that grdfill fails if both inquire and fill parameters are given.
    """
    with pytest.raises(GMTParameterError):
        grdfill(grid=grid, inquire=True, constant_fill=20)
    with pytest.raises(GMTParameterError):
        grdfill(grid=grid, inquire=True, grid_fill=grid)
    with pytest.raises(GMTParameterError):
        grdfill(grid=grid, inquire=True, neighbor_fill=True)
    with pytest.raises(GMTParameterError):
        grdfill(grid=grid, inquire=True, spline_fill=True)
    with pytest.raises(GMTParameterError):
        grdfill(grid=grid, constant_fill=20, neighbor_fill=True)
