"""
Tests for grdclip.
"""
import pytest
from pygmt import grdclip, grdinfo
from pygmt.datasets import load_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="10m", region=[-5, 5, -5, 5])


def test_grdclip_below(grid):
    """
    Test the below parameter for grdclip.
    """
    test_grid = grdclip(grid=grid, below="-1500/-1800")
    result_info = grdinfo(grid=test_grid, force_scan=0, per_column="n").strip().split()
    assert int(result_info[4]) == -1800
