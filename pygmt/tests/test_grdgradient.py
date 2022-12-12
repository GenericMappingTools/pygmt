"""
Tests for grdgradient.
"""
from pathlib import Path

import pytest
import xarray as xr
from pygmt import grdgradient, load_dataarray
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
    Load the expected grdgradient grid result.
    """
    return xr.DataArray(
        data=[
            [-1.5974800e-03, -9.9056680e-04, -6.1276241e-04, -3.6172546e-04],
            [-1.5880326e-03, -1.6113354e-03, -5.4624723e-04, -5.0047837e-04],
            [7.2569086e-04, 2.4801277e-04, 1.8859128e-05, -1.2269041e-03],
        ],
        coords=dict(
            lon=[-52.5, -51.5, -50.5, -49.5],
            lat=[-19.5, -18.5, -17.5],
        ),
        dims=["lat", "lon"],
    )


def test_grdgradient_outgrid(grid, expected_grid):
    """
    Test the azimuth and direction parameters for grdgradient with a set
    outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdgradient(
            grid=grid, outgrid=tmpfile.name, azimuth=10, region=[-53, -49, -20, -17]
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdgradient_no_outgrid(grid, expected_grid):
    """
    Test the azimuth and direction parameters for grdgradient with no set
    outgrid.

    This is a regression test for
    https://github.com/GenericMappingTools/pygmt/issues/1807.
    """
    result = grdgradient(
        grid=grid, azimuth=10, region=[-53, -49, -20, -17], outgrid=None
    )
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
