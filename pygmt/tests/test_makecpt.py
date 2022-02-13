"""
Tests for makecpt.
"""
import os

import numpy as np
import pytest
from pygmt import Figure, makecpt
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile

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


@pytest.mark.mpl_image_compare
def test_makecpt_plot_points(points, region):
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
def test_makecpt_plot_grid(region):
    """
    Use static color palette table to change color of grid.
    """
    fig = Figure()
    makecpt(cmap="relief")
    fig.colorbar(cmap=True, region=region, frame=True, position="JBC")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_plot_grid_scaled_with_series(region):
    """
    Use static color palette table scaled to a min/max series to change color
    of grid.
    """
    fig = Figure()
    makecpt(cmap="oleron", series=[0, 1000])
    fig.colorbar(cmap=True, region=region, frame=True, position="JBC")
    return fig


def test_makecpt_output_cpt_file():
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
def test_makecpt_truncated_zlow_zhigh(region):
    """
    Use static color palette table that is truncated to z-low and z-high.
    """
    fig = Figure()
    makecpt(cmap="rainbow", truncate=[0.15, 0.85], series=[0, 1000])
    fig.colorbar(cmap=True, region=region, frame=True, position="JBC")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_reverse_color_only(region):
    """
    Use static color palette table with its colors reversed.
    """
    fig = Figure()
    makecpt(cmap="earth", reverse=True, series=[0, 1000])
    fig.colorbar(cmap=True, region=region, frame=True, position="JBC")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_reverse_color_and_zsign(region):
    """
    Use static color palette table with both its colors and z-value sign
    reversed.
    """
    fig = Figure()
    makecpt(cmap="earth", reverse="cz", series=[0, 1000])
    fig.colorbar(cmap=True, region=region, frame=True, position="JBC")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_continuous(region):
    """
    Use static color palette table that is continuous from blue to white and
    scaled from -4500 to 4500m.
    """
    fig = Figure()
    makecpt(cmap="blue,white", continuous=True, series=[0, 1000])
    fig.colorbar(cmap=True, region=region, frame=True, position="JBC")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_categorical(region):
    """
    Use static color palette table that is categorical.
    """
    fig = Figure()
    makecpt(cmap="categorical", categorical=True)
    fig.colorbar(cmap=True, region=region, frame=True, position="JBC")
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_cyclic(region):
    """
    Use static color palette table that is cyclic.
    """
    fig = Figure()
    makecpt(cmap="cork", cyclic=True)
    fig.colorbar(cmap=True, region=region, frame=True, position="JBC")
    return fig


def test_makecpt_categorical_and_cyclic():
    """
    Use incorrect setting by setting both categorical and cyclic to True.
    """
    with pytest.raises(GMTInvalidInput):
        makecpt(cmap="batlow", categorical=True, cyclic=True)
