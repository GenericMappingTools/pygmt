"""
Test Figure.grdimage
"""
import numpy as np
import pytest

from .. import Figure
from ..exceptions import GMTInvalidInput
from ..datasets import load_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    "Load the grid data from the sample earth_relief file"
    return load_earth_relief(registration="gridline")


@pytest.mark.mpl_image_compare
def test_grdimage(grid):
    "Plot an image using an xarray grid"
    fig = Figure()
    fig.grdimage(grid, cmap="earth", projection="W0/6i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdimage_slice(grid):
    "Plot an image using an xarray grid that has been sliced"
    grid_ = grid.sel(lat=slice(-30, 30))
    fig = Figure()
    fig.grdimage(grid_, cmap="earth", projection="M6i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdimage_file():
    "Plot an image using file input"
    fig = Figure()
    fig.grdimage(
        "@earth_relief_01d",
        cmap="ocean",
        region=[-180, 180, -70, 70],
        projection="W0/10i",
        shading=True,
    )
    return fig


def test_grdimage_fails():
    "Should fail for unrecognized input"
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdimage(np.arange(20).reshape((4, 5)))
