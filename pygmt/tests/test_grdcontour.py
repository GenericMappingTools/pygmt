"""
Test Figure.grdcontour
"""
import os

import numpy as np
import pytest

from .. import Figure
from ..exceptions import GMTInvalidInput
from ..datasets import load_earth_relief


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_CONTOUR_FILE = os.path.join(TEST_DATA_DIR, "contours.txt")


@pytest.mark.mpl_image_compare
def test_grdcontour():
    """Plot a contour image using an xarray grid
    with fixed contour interval
    """
    grid = load_earth_relief()
    fig = Figure()
    fig.grdcontour(grid, interval="1000", projection="W0/6i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdcontour_labels():
    """Plot a contour image using a xarray grid
    with contour labels and alternate colors
    """
    grid = load_earth_relief()
    fig = Figure()
    fig.grdcontour(
        grid,
        interval="1000",
        annotation="5000",
        projection="W0/6i",
        pen=["a1p,red", "c0.5p,black"],
        label_placement="d3i",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdcontour_slice():
    "Plot an contour image using an xarray grid that has been sliced"
    grid = load_earth_relief().sel(lat=slice(-30, 30))
    fig = Figure()
    fig.grdcontour(grid, interval="1000", projection="M6i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdcontour_file():
    "Plot a contour image using grid file input"
    fig = Figure()
    fig.grdcontour(
        "@earth_relief_60m",
        interval="1000",
        limit="0",
        pen="0.5p,black",
        region=[-180, 180, -70, 70],
        projection="M10i",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdcontour_interval_file_full_opts():
    """ Plot based on external contour level file """
    fig = Figure()
    comargs = {
        "region": [-161.5, -154, 18.5, 23],
        "interval": TEST_CONTOUR_FILE,
        "grid": "@earth_relief_10m",
        "resample": "100",
        "projection": "M6i",
        "cut": 10,
    }

    fig.grdcontour(**comargs, limit=(-25000, -1), pen=["a1p,blue", "c0.5p,blue"])

    fig.grdcontour(**comargs, limit="0", pen=["a1p,black", "c0.5p,black"])
    return fig


def test_grdcontour_fails():
    "Should fail for unrecognized input"
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdcontour(np.arange(20).reshape((4, 5)))
