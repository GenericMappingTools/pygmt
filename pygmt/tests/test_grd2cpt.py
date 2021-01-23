"""
Tests for grd2cpt.
"""
import os

import numpy as np
import pytest
from pygmt import Figure, grd2cpt
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import check_figures_equal


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief()

@check_figures_equal()
def test_grd2cpt(grid):
    """
    Test the basic function of grd2cpt to create a CPT based off a grid input.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.basemap(R="0/10/0/10", J="X15c", B="a")
    grd2cpt(grid=grid)
    fig_ref.colorbar(frame="a2000")
    fig_test.basemap(region=[0, 10, 0, 10], projection="X15c", frame="a")
    grd2cpt(grid=grid)
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test

def test_grd2cpt_blank_output(grid):
    """
    Use incorrect setting by passing in blank file name to output parameter.
    """
    with pytest.raises(GMTInvalidInput):
        grd2cpt(grid=grid, output="")


def test_grd2cpt_invalid_output(grid):
    """
    Use incorrect setting by passing in invalid type to output parameter.
    """
    with pytest.raises(GMTInvalidInput):
        grd2cpt(grid=grid, output=["some.cpt"])

