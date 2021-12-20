"""
Tests for grdgradient.
"""
import os

import numpy.testing as npt
import pytest
from pygmt import grdgradient, grdinfo, load_dataarray
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
import xarray as xr


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(
        resolution="01d", registration="pixel", region=[125, 130, -25, -20]
    )


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected grdgradient grid result.
    """
    return xr.DataArray(
        data=[
            [
                -4.44407284e-04,
                -5.23089548e-04,
                -2.83417467e-04,
                -6.09701383e-04,
                -5.56207578e-06,
            ],
            [
                -3.89257970e-04,
                -1.49117477e-04,
                -1.05610132e-04,
                -4.98196052e-04,
                -2.81143642e-04,
            ],
            [
                -2.58729182e-04,
                1.10914145e-04,
                -2.62369547e-04,
                -4.26519982e-04,
                -4.27756924e-04,
            ],
            [
                -2.55958090e-04,
                -3.33979144e-04,
                -4.43578669e-04,
                7.77622772e-05,
                7.69931285e-05,
            ],
            [
                -2.86219700e-04,
                -3.75151722e-04,
                -4.55771631e-04,
                4.72632033e-04,
                -3.38737620e-04,
            ],
        ],
        coords=dict(
            lon=[125.5, 126.5, 127.5, 128.5, 129.5],
            lat=[-24.5, -23.5, -22.5, -21.5, -20.5],
        ),
        dims=["lat", "lon"],
    )


def test_grdgradient_outgrid(grid, expected_grid):
    """
    Test the azimuth and direction parameters for grdgradient with a set
    outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdgradient(grid=grid, outgrid=tmpfile.name, azimuth=10, direction="c")
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdgradient_no_outgrid(grid, expected_grid):
    """
    Test the azimuth and direction parameters for grdgradient with no set
    outgrid.
    """
    result = grdgradient(grid=grid, azimuth=10, direction="c")
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)

def test_grdgradient_fails(grid):
    """
    Check that grdgradient fails correctly.

    Check that grdgradient fails correctly when `tiles` is specified but
    normalize is not.
    """
    with pytest.raises(GMTInvalidInput):
        grdgradient(grid=grid)  # fails without required arguments
    with pytest.raises(GMTInvalidInput):
        # fails when tiles is specified but not normalize
        grdgradient(grid=grid, azimuth=10, direction="c", tiles="c")
