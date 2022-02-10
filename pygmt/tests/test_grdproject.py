"""
Tests for grdproject.
"""
import os

import pytest
import xarray as xr
from pygmt import grdproject, load_dataarray
from pygmt.helpers.testing import load_static_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected grdproject grid result.
    """
    return xr.DataArray(
        data=[
            [442.91666, 439.51202, 462.82422, 504.1126, 508.01578],
            [393.78897, 364.91565, 415.91202, 449.7487, 507.4866],
            [362.80795, 400.7865, 423.06854, 374.5926, 403.55084],
            [322.25696, 378.78528, 362.4327, 355.9475, 422.6374],
            [282.81348, 318.37677, 326.95657, 379.11594, 383.81543],
        ],
        coords=dict(
            x=[1.0, 3.0, 5.0, 7.0, 9.0],
            y=[1.076665, 3.229995, 5.383325, 7.536655, 9.689984],
        ),
        dims=["y", "x"],
    )


def test_grdproject_file_out(grid, expected_grid):
    """
    grdproject with an outgrid set.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdproject(grid=grid, projection="M10c", outgrid=tmpfile.name)
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        print(temp_grid)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdproject_no_outgrid(grid, expected_grid):
    """
    Test grdproject with no set outgrid.
    """
    assert grid.gmt.gtype == 1  # Geographic grid
    result = grdproject(grid=grid, projection="M10c")
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
