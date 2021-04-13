"""
Tests for grd2cpt.
"""
import os

import pytest
from pygmt import Figure, grd2cpt
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief()


@pytest.mark.mpl_image_compare
def test_grd2cpt(grid):
    """
    Test creating a CPT with grd2cpt to create a CPT based off a grid input and
    plot it with a color bar.
    """
    fig = Figure()
    fig.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid)
    fig.colorbar(frame="a2000")
    return fig


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


def test_grd2cpt_output_to_cpt_file(grid):
    """
    Save the generated static color palette table to a .cpt file.
    """
    with GMTTempFile(suffix=".cpt") as cptfile:
        grd2cpt(grid=grid, output=cptfile.name)
        assert os.path.getsize(cptfile.name) > 0


def test_grd2cpt_unrecognized_data_type():
    """
    Test that an error will be raised if an invalid data type is passed to
    grid.
    """
    with pytest.raises(GMTInvalidInput):
        grd2cpt(grid=0)


def test_grd2cpt_categorical_and_cyclic(grid):
    """
    Use incorrect setting by setting both categorical and cyclic to True.
    """
    with pytest.raises(GMTInvalidInput):
        grd2cpt(grid=grid, cmap="batlow", categorical=True, cyclic=True)
