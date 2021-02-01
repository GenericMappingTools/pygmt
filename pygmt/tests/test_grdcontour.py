"""
Test Figure.grdcontour.
"""
import os

import numpy as np
import pytest
from pygmt import Figure
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.testing import check_figures_equal

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_CONTOUR_FILE = os.path.join(TEST_DATA_DIR, "contours.txt")


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(registration="gridline")


@check_figures_equal()
def test_grdcontour(grid):
    """
    Plot a contour image using an xarray grid with fixed contour interval.
    """
    fig_ref, fig_test = Figure(), Figure()
    kwargs = dict(interval="1000", projection="W0/6i")
    fig_ref.grdcontour("@earth_relief_01d_g", **kwargs)
    fig_test.grdcontour(grid, **kwargs)
    return fig_ref, fig_test


@check_figures_equal()
def test_grdcontour_labels(grid):
    """
    Plot a contour image using a xarray grid with contour labels and alternate
    colors.
    """
    fig_ref, fig_test = Figure(), Figure()
    kwargs = dict(
        interval="1000",
        annotation="5000",
        projection="W0/6i",
        pen=["a1p,red", "c0.5p,black"],
        label_placement="d3i",
    )
    fig_ref.grdcontour("@earth_relief_01d_g", **kwargs)
    fig_test.grdcontour(grid, **kwargs)
    return fig_ref, fig_test


@check_figures_equal()
def test_grdcontour_slice(grid):
    """
    Plot an contour image using an xarray grid that has been sliced.
    """

    fig_ref, fig_test = Figure(), Figure()

    grid_ = grid.sel(lat=slice(-30, 30))
    kwargs = dict(interval="1000", projection="M6i")
    fig_ref.grdcontour(
        grid="@earth_relief_01d_g", region=[-180, 180, -30, 30], **kwargs
    )
    fig_test.grdcontour(grid=grid_, **kwargs)
    return fig_ref, fig_test


@pytest.mark.mpl_image_compare
def test_grdcontour_file():
    """
    Plot a contour image using grid file input.
    """
    fig = Figure()
    fig.grdcontour(
        "@earth_relief_01d_g",
        interval="1000",
        limit="0",
        pen="0.5p,black",
        region=[-180, 180, -70, 70],
        projection="M10i",
    )
    return fig


@check_figures_equal()
def test_grdcontour_interval_file_full_opts():
    """
    Plot based on external contour level file.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    comargs_ref = {
        "grid": "@earth_relief_10m",
        "R": "-161.5/-154/18.5/23",
        "C": TEST_CONTOUR_FILE,
        "S": 100,
        "J": "M6i",
        "Q": 10,
    }
    fig_ref.grdcontour(**comargs_ref, L="-25000/-1", W=["a1p,blue", "c0.5p,blue"])
    fig_ref.grdcontour(**comargs_ref, L="0", W=["a1p,black", "c0.5p,black"])

    comargs_test = {
        "region": [-161.5, -154, 18.5, 23],
        "interval": TEST_CONTOUR_FILE,
        "grid": "@earth_relief_10m",
        "resample": "100",
        "projection": "M6i",
        "cut": 10,
    }
    fig_test.grdcontour(
        **comargs_test, limit=(-25000, -1), pen=["a1p,blue", "c0.5p,blue"]
    )
    fig_test.grdcontour(**comargs_test, limit=0, pen=["a1p,black", "c0.5p,black"])

    return fig_ref, fig_test


def test_grdcontour_fails():
    """
    Should fail for unrecognized input.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdcontour(np.arange(20).reshape((4, 5)))
