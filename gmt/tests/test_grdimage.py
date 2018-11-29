"""
Test Figure.grdimage
"""
import numpy as np
import pytest

from .. import Figure
from ..exceptions import GMTInvalidInput
from ..datasets import load_earth_relief


@pytest.mark.mpl_image_compare
def test_grdimage():
    "Plot an image using an xarray grid"
    grid = load_earth_relief()
    fig = Figure()
    fig.grdimage(grid, cmap="earth", projection="W0/6i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdimage_slice():
    "Plot an image using an xarray grid that has been sliced"
    grid = load_earth_relief().sel(lat=slice(-30, 30))
    fig = Figure()
    fig.grdimage(grid, cmap="earth", projection="M6i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdimage_file():
    "Plot an image using file input"
    fig = Figure()
    fig.grdimage(
        "@earth_relief_60m",
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
