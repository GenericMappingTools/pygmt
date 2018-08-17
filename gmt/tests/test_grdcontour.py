"""
Test Figure.grdcontour
"""
import pytest
import numpy as np

from .. import Figure
from ..exceptions import GMTInvalidInput
from ..datasets import load_earth_relief

@pytest.mark.mpl_image_compare
def test_grdcontour():
    """Plot a contour image using an xarray grid
    with fixed contour interval
    """    
    grid = load_earth_relief()
    fig = Figure()
    fig.grdcontour(grid,
                   contour_interval="1000",
                   projection="W0/6i")
    return fig

@pytest.mark.mpl_image_compare
def test_grdcontour_labels():
    """Plot a contour image using a xarray grid
    with contour labels and alternate colors
    """
    grid = load_earth_relief()
    fig = Figure()
    fig.grdcontour(grid,
                   contour_interval="1000",
                   annotation_interval="5000",
                   projection="W0/6i",
                   pen=["a1p,red","c0.5p,black"],
                   label_placement="d3i",
                   )
    return fig


@pytest.mark.mpl_image_compare
def test_grdcontour_slice():
    "Plot an contour image using an xarray grid that has been sliced"
    grid = load_earth_relief().sel(lat=slice(-30, 30))
    fig = Figure()
    fig.grdcontour(grid,
                   contour_interval="1000",
                   projection="M6i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdcontour_file():
    "Plot a contour image using grid file input"
    fig = Figure()
    fig.grdcontour(
        "@earth_relief_60m",
        contour_interval="1000",
        limit="0",
        pen="0.5p,black",
        region=[-180, 180, -70, 70],
        projection="M10i",
    )
    return fig


def test_grdcontour_fails():
    "Should fail for unrecognized input"
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdcontour(np.arange(20).reshape((4, 5)))
