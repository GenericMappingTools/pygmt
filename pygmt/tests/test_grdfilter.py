"""
Tests for grdfilter.
"""
from pathlib import Path

import numpy as np
import pytest
import xarray as xr
from pygmt import grdfilter, load_dataarray
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static earth relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected grdfilter grid result.
    """
    return xr.DataArray(
        data=[
            [502.61914, 488.27576, 494.10657, 559.06244],
            [614.6496, 601.4992, 569.9743, 606.0966],
            [661.41003, 656.9681, 625.1668, 664.40204],
        ],
        coords=dict(
            lon=[-52.5, -51.5, -50.5, -49.5],
            lat=[-19.5, -18.5, -17.5],
        ),
        dims=["lat", "lon"],
    )


def test_grdfilter_dataarray_in_dataarray_out(grid, expected_grid):
    """
    Test grdfilter with an input DataArray, and output as DataArray.
    """
    result = grdfilter(
        grid=grid, filter="g600", distance="4", region=[-53, -49, -20, -17]
    )
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdfilter_dataarray_in_file_out(grid, expected_grid):
    """
    Test grdfilter with an input DataArray, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdfilter(
            grid,
            outgrid=tmpfile.name,
            filter="g600",
            distance="4",
            region=[-53, -49, -20, -17],
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdfilter_fails():
    """
    Check that grdfilter fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdfilter(np.arange(10).reshape((5, 2)))
