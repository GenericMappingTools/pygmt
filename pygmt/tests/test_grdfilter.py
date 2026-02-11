"""
Test pygmt.grdfilter.
"""

from pathlib import Path

import numpy as np
import pytest
import xarray as xr
from pygmt import grdfilter
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTParameterError, GMTTypeError
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
        coords={
            "lon": [-52.5, -51.5, -50.5, -49.5],
            "lat": [-19.5, -18.5, -17.5],
        },
        dims=["lat", "lon"],
    )


@pytest.mark.benchmark
def test_grdfilter_dataarray_in_dataarray_out(grid, expected_grid):
    """
    Test grdfilter with an input DataArray, and output as DataArray.
    """
    result = grdfilter(
        grid=grid,
        filter="g600",
        distance="geo_spherical",
        region=[-53, -49, -20, -17],
        cores=2,
    )
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype is GridType.GEOGRAPHIC
    assert result.gmt.registration is GridRegistration.PIXEL
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
            distance="geo_spherical",
            region=[-53, -49, -20, -17],
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
        temp_grid = xr.load_dataarray(tmpfile.name, engine="gmt", raster_kind="grid")
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdfilter_fails():
    """
    Check that grdfilter fails correctly.
    """
    with pytest.raises(GMTTypeError):
        grdfilter(
            np.arange(10).reshape((5, 2)), filter="g600", distance="geo_spherical"
        )


def test_grdfilter_required(grid):
    """
    Test that grdfilter raises an exception when required parameters are missing.
    """
    with pytest.raises(GMTParameterError, match="distance"):
        grdfilter(grid=grid, filter="g600")
