"""
Tests for dimfilter.
"""
from pathlib import Path

import pytest
import xarray as xr
from pygmt import dimfilter, load_dataarray
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
    Load the expected dimfilter grid result.
    """
    return xr.DataArray(
        data=[
            [346.0, 344.5, 349.0, 349.0],
            [344.5, 318.5, 344.5, 394.0],
            [344.5, 356.5, 345.5, 352.5],
            [367.5, 349.0, 385.5, 349.0],
            [435.0, 385.5, 413.5, 481.5],
        ],
        coords=dict(
            lon=[-54.5, -53.5, -52.5, -51.5],
            lat=[-23.5, -22.5, -21.5, -20.5, -19.5],
        ),
        dims=["lat", "lon"],
    )


def test_dimfilter_outgrid(grid, expected_grid):
    """
    Test the required parameters for dimfilter with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = dimfilter(
            grid=grid,
            outgrid=tmpfile.name,
            filter="m600",
            distance=4,
            sectors="l6",
            region=[-55, -51, -24, -19],
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_dimfilter_no_outgrid(grid, expected_grid):
    """
    Test the required parameters for dimfilter with no set outgrid.
    """
    result = dimfilter(
        grid=grid, filter="m600", distance=4, sectors="l6", region=[-55, -51, -24, -19]
    )
    assert result.dims == ("lat", "lon")
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_dimfilter_fails(grid):
    """
    Check that dimfilter fails correctly when not all of sectors, filters, and
    distance are specified.
    """
    with pytest.raises(GMTInvalidInput):
        dimfilter(grid=grid, sectors="l6", distance=4)
