"""
Tests for grdproject.
"""
from pathlib import Path

import pytest
import xarray as xr
from pygmt import grdproject, load_dataarray
from pygmt.exceptions import GMTInvalidInput
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
    Load the expected grdproject grid result.
    """
    return xr.DataArray(
        data=[
            [427.85062, 431.05698, 452.34268],
            [563.92957, 540.5212, 501.46896],
            [740.80133, 679.1116, 554.78534],
            [794.233, 829.4449, 764.12225],
            [749.37445, 834.55994, 831.2627],
        ],
        coords=dict(
            x=[1.666667, 5.0, 8.333333],
            y=[1.572432, 4.717295, 7.862158, 11.007022, 14.151885],
        ),
        dims=["y", "x"],
    )


def test_grdproject_file_out(grid, expected_grid):
    """
    grdproject with an outgrid set.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdproject(
            grid=grid,
            projection="M10c",
            outgrid=tmpfile.name,
            spacing=3,
            region=[-53, -51, -20, -17],
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


@pytest.mark.parametrize(
    "projection",
    ["M10c", "EPSG:3395 +width=10", "+proj=merc +ellps=WGS84 +units=m +width=10"],
)
def test_grdproject_no_outgrid(grid, projection, expected_grid):
    """
    Test grdproject with no set outgrid.

    Also check that providing the projection as an EPSG code or PROJ4 string
    works.
    """
    assert grid.gmt.gtype == 1  # Geographic grid
    result = grdproject(
        grid=grid, projection=projection, spacing=3, region=[-53, -51, -20, -17]
    )
    assert result.gmt.gtype == 0  # Rectangular grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdproject_fails(grid):
    """
    Check that grdproject fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdproject(grid=grid)
