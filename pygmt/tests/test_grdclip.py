"""
Tests for grdclip.
"""
import os

import pytest
from pygmt import grdclip, grdinfo
from pygmt.datasets import load_earth_relief
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="10m", region=[-5, 5, -5, 5])


def test_grdclip(grid):
    """
    Test the below and above parameters for grdclip.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdclip(
            grid=grid, outgrid=tmpfile.name, below="-1500/-1800", above="30/40"
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = (
            grdinfo(grid=tmpfile.name, force_scan=0, per_column="n").strip().split()
        )
    assert int(result[4]) == -1800
    assert int(result[5]) == 40
