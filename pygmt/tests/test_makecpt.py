"""
Tests for makecpt.
"""
import os
from pathlib import Path

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


@pytest.fixture(scope="module", name="position")
def fixture_position():
    """
    Return a standard position argument for the colorbar.
    """
    return "x0c/0c+w10c+h"


@pytest.mark.mpl_image_compare
def test_makecpt_plot_points(points):
    """
    Use static color palette table to change color of points.
    """
    fig = Figure()
    makecpt(cmap="rainbow")
    fig.plot(
        x=points[:, 0],
        y=points[:, 1],
        fill=points[:, 2],
        region=[10, 70, -5, 10],
        style="c1c",
        cmap=True,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_plot_colorbar(position):
    """
    Use static color palette table to plot a colorbar.
    """
    fig = Figure()
    makecpt(cmap="relief")
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_plot_colorbar_scaled_with_series(position):
    """
    Use static color palette table scaled to a min/max series and plot it on a
    colorbar.
    """
    fig = Figure()
    makecpt(cmap="oleron", series=[0, 1000])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


def test_makecpt_output_cpt_file():
    """
    Save the generated static color palette table to a .cpt file.
    """
    with GMTTempFile(suffix=".cpt") as cptfile:
        makecpt(output=cptfile.name)
        assert Path(cptfile.name).stat().st_size > 0


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
def test_makecpt_truncated_zlow_zhigh(position):
    """
    Use static color palette table that is truncated to z-low and z-high.
    """
    fig = Figure()
    makecpt(cmap="rainbow", truncate=[0.15, 0.85], series=[0, 1000])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_reverse_color_only(position):
    """
    Use static color palette table with its colors reversed.
    """
    fig = Figure()
    makecpt(cmap="earth", reverse=True, series=[0, 1000])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_reverse_color_and_zsign(position):
    """
    Use static color palette table with both its colors and z-value sign
    reversed.
    """
    fig = Figure()
    makecpt(cmap="earth", reverse="cz", series=[0, 1000])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_continuous(position):
    """
    Use static color palette table that is continuous from blue to white and
    scaled from 0 to 1000 m.
    """
    fig = Figure()
    makecpt(cmap="blue,white", continuous=True, series=[0, 1000])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_categorical(position):
    """
    Use static color palette table that is categorical.
    """
    fig = Figure()
    makecpt(cmap="categorical", categorical=True, series=[0, 6, 1])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_cyclic(position):
    """
    Use static color palette table that is cyclic.
    """
    fig = Figure()
    makecpt(cmap="cork", cyclic=True)
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


def test_makecpt_categorical_and_cyclic():
    """
    Use incorrect setting by setting both categorical and cyclic to True.
    """
    with pytest.raises(GMTInvalidInput):
        makecpt(cmap="batlow", categorical=True, cyclic=True)
