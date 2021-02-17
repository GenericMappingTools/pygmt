"""
Tests for makecpt.
"""
import os

import numpy as np
import pytest
from pygmt import Figure, makecpt
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
    return [10, 70, -5, 10]


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(registration="gridline")


@pytest.mark.mpl_image_compare
def test_makecpt_to_plot_points(points, region):
    """
    Use static color palette table to change color of points.
    """
    fig = Figure()
    makecpt(cmap="rainbow")
    fig.plot(
        x=points[:, 0],
        y=points[:, 1],
        color=points[:, 2],
        region=region,
        style="c1c",
        cmap=True,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_to_plot_grid(grid):
    """
    Use static color palette table to change color of grid.
    """
    fig = Figure()
    makecpt(cmap="relief")
    fig.grdimage(grid, projection="W0/6i")
    return fig


@check_figures_equal()
def test_makecpt_to_plot_grid_scaled_with_series(grid):
    """
    Use static color palette table scaled to a min/max series to change color
    of grid.
    """
    # Use single-character arguments for the reference image
    fig_ref = Figure()
    makecpt(C="oleron", T="-4500/4500")
    fig_ref.grdimage(grid, J="W0/6i")

    fig_test = Figure()
    makecpt(cmap="oleron", series="-4500/4500")
    fig_test.grdimage(grid, projection="W0/6i")
    return fig_ref, fig_test


def test_makecpt_output_to_cpt_file():
    """
    Save the generated static color palette table to a .cpt file.
    """
    with GMTTempFile(suffix=".cpt") as cptfile:
        makecpt(output=cptfile.name)
        assert os.path.exists(cptfile.name)


def test_makecpt_blank_output():
    """
    Use incorrect setting by passing in blank file name to output parameter.
    """
    with pytest.raises(GMTInvalidInput):
        makecpt(output="")


def test_makecpt_invalid_output():
    """
    Use incorrect setting by passing in invalid type to output parameter.
    """
    with pytest.raises(GMTInvalidInput):
        makecpt(output=["some.cpt"])


@pytest.mark.mpl_image_compare
def test_makecpt_truncated_to_zlow_zhigh(grid):
    """
    Use static color palette table that is truncated to z-low and z-high.
    """
    fig = Figure()
    makecpt(cmap="rainbow", truncate=[0.15, 0.85], series=[-4500, 4500])
    fig.grdimage(grid, projection="W0/6i")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_truncated_at_zlow_only(grid):
    """
    Use static color palette table that is truncated at z-low only.
    """
    fig = Figure()
    makecpt(cmap="rainbow", truncate=[0.5, None], series=[-4500, 4500])
    fig.grdimage(grid, projection="W0/6i")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_truncated_at_zhigh_only(grid):
    """
    Use static color palette table that is truncated at z-high only.
    """
    fig = Figure()
    makecpt(cmap="rainbow", truncate=[None, 0.5], series=[-4500, 4500])
    fig.grdimage(grid, projection="W0/6i")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_reverse_color_only(grid):
    """
    Use static color palette table with its colors reversed.
    """
    fig = Figure()
    makecpt(cmap="earth", reverse=True)
    fig.grdimage(grid, projection="W0/6i")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_reverse_zsign_only(grid):
    """
    Use static color palette table with its z-value sign reversed.
    """
    fig = Figure()
    makecpt(cmap="earth", reverse="z")
    fig.grdimage(grid, projection="W0/6i")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_reverse_color_and_zsign(grid):
    """
    Use static color palette table with both its colors and z-value sign
    reversed.
    """
    fig = Figure()
    makecpt(cmap="earth", reverse="cz")
    fig.grdimage(grid, projection="W0/6i")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_continuous(grid):
    """
    Use static color palette table that is continuous from blue to white and
    scaled from -4500 to 4500m.
    """
    fig = Figure()
    makecpt(cmap="blue,white", continuous=True, series="-4500,4500")
    fig.grdimage(grid, projection="W0/6i")
    return fig


@check_figures_equal()
def test_makecpt_categorical(region):
    """
    Use static color palette table that is categorical.
    """
    fig_ref = Figure()
    makecpt(C="categorical", W="")
    fig_ref.colorbar(cmap=True, region=region, frame=True, position="JBC")

    fig_test = Figure()
    makecpt(cmap="categorical", categorical=True)
    fig_test.colorbar(cmap=True, region=region, frame=True, position="JBC")
    return fig_ref, fig_test


@check_figures_equal()
def test_makecpt_cyclic(region):
    """
    Use static color palette table that is cyclic.
    """
    fig_ref = Figure()
    makecpt(C="cork", W="w")
    fig_ref.colorbar(cmap=True, region=region, frame=True, position="JBC")

    fig_test = Figure()
    makecpt(cmap="cork", cyclic=True)
    fig_test.colorbar(cmap=True, region=region, frame=True, position="JBC")
    return fig_ref, fig_test


def test_makecpt_categorical_and_cyclic():
    """
    Use incorrect setting by setting both categorical and cyclic to True.
    """
    with pytest.raises(GMTInvalidInput):
        makecpt(cmap="batlow", categorical=True, cyclic=True)
