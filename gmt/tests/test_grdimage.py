"""
Test Figure.grdimage
"""
import pytest
import numpy as np

from .. import Figure
from ..exceptions import GMTInvalidInput
from ..datasets import load_earth_relief


@pytest.mark.mpl_image_compare
def test_grdimage_file():
    "Plot an image using file input"
    fig = Figure()
    fig.grdimage(
        "@earth_relief_60m",
        cmap="ocean",
        region="-180/180/-70/70",
        projection="W0/10i",
        shading=True,
    )
    return fig


def test_grdimage_fails():
    "Should fail for unrecognized input"
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdimage(np.arange(20).reshape((4, 5)))
    grid = load_earth_relief()
    with pytest.raises(NotImplementedError):
        fig.grdimage(grid)
