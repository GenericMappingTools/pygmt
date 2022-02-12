"""
Tests for grdinfo.
"""
import numpy as np
import pytest
from pygmt import grdinfo
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file.
    """
    return load_static_earth_relief()


def test_grdinfo(grid):
    """
    Make sure grdinfo works as expected.
    """
    result = grdinfo(grid=grid, force_scan=0, per_column="n")
    assert result.strip() == "-55 -47 -24 -10 190 981 1 1 8 14 1 1"


def test_grdinfo_fails():
    """
    Check that grdinfo fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdinfo(np.arange(10).reshape((5, 2)))


def test_grdinfo_region(grid):
    """
    Check that the region argument works in grdinfo.
    """
    result = grdinfo(
        grid=grid, force_scan=0, per_column="n", region=[-54, -50, -23, -20]
    )
    assert result.strip() == "-54 -50 -23 -20 284.5 491 1 1 4 3 1 1"
