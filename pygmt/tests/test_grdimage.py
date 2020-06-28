# pylint: disable=redefined-outer-name
"""
Test Figure.grdimage
"""
import numpy as np
import xarray as xr
import pytest

from .. import Figure
from ..exceptions import GMTInvalidInput
from ..datasets import load_earth_relief


@pytest.fixture(scope="module")
def xrgrid():
    """
    Create a sample xarray.DataArray grid for testing
    """
    longitude = np.arange(0, 360, 1)
    latitude = np.arange(-89, 91, 1)
    x = np.sin(np.deg2rad(longitude))
    y = np.linspace(start=0, stop=1, num=180)
    data = y[:, np.newaxis] * x

    return xr.DataArray(
        data,
        coords=[
            ("latitude", latitude, {"units": "degrees_north"}),
            ("longitude", longitude, {"units": "degrees_east"}),
        ],
        attrs={"actual_range": [-1, 1]},
    )


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


@pytest.mark.mpl_image_compare
def test_grdimage_over_dateline(xrgrid):
    """
    Ensure no gaps are plotted over the 180 degree international dateline.
    Specifically checking that coord_sys="g" sets `GMT_GRID_IS_GEO`, and that
    node_offset=1 sets `GMT_GRID_PIXEL_REG`. Works for GMT > 6.1.0.
    """
    fig = Figure()
    xrgrid.attrs["node_offset"] = 1
    fig.grdimage(grid=xrgrid, region="g", projection="A0/0/1i", coord_sys="c")
    return fig
