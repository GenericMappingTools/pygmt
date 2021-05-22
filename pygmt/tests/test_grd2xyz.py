"""
Tests for grd2xyz.
"""
import pytest
from pygmt import grd2xyz
from pygmt.datasets import load_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[-1, 1, -1, 1])


def test_grd2xyz(grid):
    """
    Make sure grd2xyz works as expected.
    """
    xyz_data = grd2xyz(grid=grid)
    assert xyz_data.strip().split("\n") == [
        "-0.5 0.5 -4967",
        "0.5 0.5 -4852",
        "-0.5 -0.5 -4917",
        "0.5 -0.5 -4747.5",
    ]
