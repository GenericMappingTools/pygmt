"""
Tests for grdsample.
"""
import os

import pytest
from pygmt import grdinfo, grdsample
from pygmt.datasets import load_earth_relief
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(
        resolution="01d", region=[-5, 5, -5, 5], registration="pixel"
    )


def test_grdsample_file_out(grid):
    """
    grdsample with an outgrid set and the spacing is changed.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdsample(grid=grid, outgrid=tmpfile.name, spacing=[1, 0.5])
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = grdinfo(tmpfile.name, per_column=True).strip().split()
        assert float(result[6]) == 1  # x-increment
        assert float(result[7]) == 0.5  # y-increment


def test_grdsample_no_outgrid(grid):
    """
    Test grdsample with no set outgrid and applying registration changes.
    """
    assert grid.gmt.registration == 1  # Pixel registration
    translated_grid = grdsample(grid=grid, translate=True)
    assert translated_grid.gmt.registration == 0  # Gridline registration
    registration_grid = grdsample(grid=translated_grid, registration="p")
    assert registration_grid.gmt.registration == 1  # Pixel registration
