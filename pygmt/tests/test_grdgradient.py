"""
Tests for grdgradient.
"""
import os

import numpy.testing as npt
import pytest
from pygmt import grdgradient, grdinfo
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[-5, 5, -5, 5])


def test_grdgradient_outgrid(grid):
    """
    Test the azimuth and direction parameters for grdgradient with a set
    outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdgradient(grid=grid, outgrid=tmpfile.name, azimuth=10, direction="c")
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = (
            grdinfo(grid=tmpfile.name, force_scan=0, per_column="n").strip().split()
        )
    npt.assert_allclose(float(result[4]), -0.0045060496)
    npt.assert_allclose(float(result[5]), 0.0575332976)


def test_grdgradient_no_outgrid(grid):
    """
    Test the azimuth and direction parameters for grdgradient with no set
    outgrid.
    """
    temp_grid = grdgradient(grid=grid, azimuth=10, direction="c")
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 1  # Pixel registration
    npt.assert_allclose(temp_grid.min(), -0.0045060496)
    npt.assert_allclose(temp_grid.max(), 0.0575332976)


def test_grdgradient_fails(grid):
    """
    Check that grdgradient fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdgradient(grid=grid)
