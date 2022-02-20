"""
Test Figure.grdcontour.
"""
import os

import numpy as np
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.testing import load_static_earth_relief

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_CONTOUR_FILE = os.path.join(TEST_DATA_DIR, "contours.txt")


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file.
    """
    return load_static_earth_relief()


@pytest.mark.mpl_image_compare
def test_grdcontour(grid):
    """
    Plot a contour image using an xarray grid with fixed contour interval.
    """
    fig = Figure()
    fig.grdcontour(
        grid=grid, interval=50, annotation=200, projection="M10c", frame=True
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdcontour_labels(grid):
    """
    Plot a contour image using a xarray grid with contour labels and alternate
    colors.
    """
    fig = Figure()
    fig.grdcontour(
        grid=grid,
        interval=50,
        annotation=200,
        projection="M10c",
        pen=["a1p,red", "c0.5p,black"],
        label_placement="d6c",
        frame=True,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdcontour_slice(grid):
    """
    Plot an contour image using an xarray grid that has been sliced.
    """
    grid_ = grid.sel(lat=slice(-20, -10))

    fig = Figure()
    fig.grdcontour(grid=grid_, interval=100, projection="M10c", frame=True)
    return fig


@pytest.mark.mpl_image_compare
def test_grdcontour_interval_file_full_opts(grid):
    """
    Plot based on external contour level file.
    """
    fig = Figure()

    comargs = {
        "region": [-53, -49, -20, -17],
        "interval": TEST_CONTOUR_FILE,
        "grid": grid,
        "resample": 100,
        "projection": "M10c",
        "cut": 10,
    }
    # Plot contours below 650 in blue
    fig.grdcontour(
        **comargs, limit=(0, 649), pen=["a1p,blue", "c0.5p,blue"], frame=True
    )
    # Plot contours above 650 in black
    fig.grdcontour(**comargs, limit=(650, 1000), pen=["a1p,black", "c0.5p,black"])

    return fig


def test_grdcontour_fails():
    """
    Should fail for unrecognized input.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdcontour(np.arange(20).reshape((4, 5)))
