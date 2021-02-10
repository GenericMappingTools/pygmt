"""
Tests for grd2cpt.
"""
import os

import numpy as np
import pytest
from pygmt import Figure
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import check_figures_equal
from pygmt.src.grd2cpt import grd2cpt

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
    return load_earth_relief()


@check_figures_equal()
def test_grd2cpt(grid):
    """
    Test creating a CPT with grd2cpt to create a CPT based off a grid input and
    plot it with a color bar.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid="@earth_relief_01d")
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid)
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_to_plot_points(points, region, grid):
    """
    Use CPT to change color of points.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(R=region, J="X15c", B="a")
    grd2cpt(grid=grid, C="rainbow")
    fig_ref.plot(
        x=points[:, 0], y=points[:, 1], G=points[:, 2], R=region, S="c1c", C=True
    )
    fig_test.basemap(region=region, projection="X15c", frame="a")
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


@check_figures_equal()
def test_grd2cpt_set_cpt(grid):
    """
    Test function grd2cpt to create a CPT based off a grid input and a set CPT.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, cmap="rainbow")
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="rainbow")
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_scaled_with_series(grid):
    """
    Create CPT scaled to a min/max series to change color of grid.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, cmap="rainbow", T="-4500/4500/500")
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="rainbow", series=[-4500, 4500, 500])
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_truncated_to_zlow_zhigh(grid):
    """
    Create CPT that is truncated to z-low and z-high.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, cmap="rainbow", G="0.15/0.85", T="-4500/4500/500")
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="rainbow", truncate=[0.15, 0.85], series=[-4500, 4500, 500])
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_truncated_to_zlow_only(grid):
    """
    Create CPT that is truncated at z-low only.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, cmap="rainbow", G="0.5/NaN", T="-4500/4500/500")
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="rainbow", truncate=[0.5, None], series=[-4500, 4500, 500])
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_truncated_to_zhigh_only(grid):
    """
    Create CPT that is truncated at z-high only.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, cmap="rainbow", G="NaN/0.5", T="-4500/4500/500")
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="rainbow", truncate=[None, 0.5], series=[-4500, 4500, 500])
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_reverse_color_only(grid):
    """
    Create CPT with its colors reversed.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, C="rainbow", I=True)
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="rainbow", reverse=True)
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_reverse_zsign_only(grid):
    """
    Create CPT with its z-value sign reversed.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, C="earth", I="z")
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="earth", reverse="z")
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_reverse_color_and_zsign(grid):
    """
    Create CPT with its colors and z-value sign reversed.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, C="earth", I="cz")
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="earth", reverse="cz")
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_continuous(grid):
    """
    Create a CPT with that is continuous.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, C="blue,white", Z=True)
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="blue,white", continuous=True)
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_categorical(grid):
    """
    Create a CPT with that is categorical.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, C="geo", W=True)
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="geo", categorical=True)
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_cyclic(grid):
    """
    Create a CPT with that is cyclic.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, C="geo", Ww=True)
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="geo", cyclic=True)
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_limit(grid):
    """
    Create a CPT with that sets a min/max limit.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid=grid, C="haxby", L="-1000/1000")
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, cmap="haxby", limit=[-1000, 1000])
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


@check_figures_equal()
def test_grd2cpt_nlevels_number(grid):
    """
    Set number of equidistant slices with nlevels alias in CPT.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid="@earth_relief_01d", E="10")
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, nlevels=10)
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test


@check_figures_equal()
def test_grd2cpt_nlevels_bool(grid):
    """
    Set equidistant slices with nlevels alias in CPT.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(B="a", J="W0/15c", R="d")
    grd2cpt(grid="@earth_relief_01d", E="")
    fig_ref.colorbar(B="a2000")
    fig_test.basemap(frame="a", projection="W0/15c", region="d")
    grd2cpt(grid=grid, nlevels=True)
    fig_test.colorbar(frame="a2000")
    return fig_ref, fig_test
