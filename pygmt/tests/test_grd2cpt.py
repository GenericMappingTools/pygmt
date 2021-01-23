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

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")


@pytest.fixture(scope="module", name="points")
def fixture_points():
    """
    Load the points data from the test file.
    """
    return np.loadtxt(POINTS_DATA)


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    The data region.
    """
    return [0, 10, 0, 10]


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(registration="gridline")


@check_figures_equal()
def test_grd2cpt(grid, region):
    """
    Test the basic function of grd2cpt to create a CPT based off a grid input.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.basemap(R=region, J="X15c", B="a")
    grd2cpt(grid=grid)
    fig_ref.colorbar(frame="a2000")
    fig_test.basemap(region=region, projection="X15c", frame="a")
    grd2cpt(grid=grid)
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_grdimage(grid, region):
    """
    Test creating a CPT with grd2cpt and plot it with grdimage.
    """
    fig_ref, fig_test = Figure(), Figure()
    grd2cpt(grid=grid, cmap="rainbow", continuous=True)
    fig_ref.grdimage(grid, projection="W0/15c")
    fig_ref.colorbar(frame="a2000")
    grd2cpt(grid=grid, cmap="rainbow", continuous=True)
    fig_test.grdimage(grid, projection="W0/15c")
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_to_plot_points(points, region, grid):
    """
    Use color palette table to change color of points.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.basemap(R=[10, 70, -5, 10], J="X15c", B="a")
    grd2cpt(grid=grid, C="rainbow")
    fig_ref.plot(
        x=points[:, 0],
        y=points[:, 1],
        color=points[:, 2],
        region=region,
        style="c1c",
        cmap=True,
    )
    fig_test.basemap(region=[10, 70, -5, 10], projection="X15c", frame="a")
    grd2cpt(grid=grid, cmap="rainbow")
    fig_test.plot(
        x=points[:, 0],
        y=points[:, 1],
        color=points[:, 2],
        region=region,
        style="c1c",
        cmap=True,
    )
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


def test_grd2cpt_output_to_cpt_file(grid):
    """
    Save the generated static color palette table to a .cpt file.
    """
    with GMTTempFile(suffix=".cpt") as cptfile:
        grd2cpt(grid=grid, output=cptfile.name)
        assert os.path.exists(cptfile.name)


@check_figures_equal()
def test_grd2cpt_set_cpt(grid, region):
    """
    Test function grd2cpt to create a CPT based off a grid input and a set CPT.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.basemap(R=region, J="X15c", B="a")
    grd2cpt(grid=grid, cmap="rainbow")
    fig_ref.colorbar(frame="a2000")

    fig_test.basemap(region=region, projection="X15c", frame="a")
    grd2cpt(grid=grid, cmap="rainbow")
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_truncated_to_zlow_zhigh(grid, region):
    """
    Test the basic function of grd2cpt to create a CPT based off a grid input.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.basemap(region=[0, 10, 0, 10], projection="X15c", frame="a")
    grd2cpt(grid=grid, cmap="rainbow", truncate="0.15/0.85", series="-4500/4500/500")
    fig_ref.colorbar(frame="a2000")
    fig_test.basemap(region=[0, 10, 0, 10], projection="X15c", frame="a")
    grd2cpt(grid=grid, cmap="rainbow", truncate="0.15/0.85", series="-4500/4500/500")
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test
