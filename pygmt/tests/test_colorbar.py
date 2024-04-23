"""
Test Figure.colorbar.
"""

import pytest
from pygmt import Figure


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_colorbar():
    """
    Create a simple colorbar.
    """
    fig = Figure()
    fig.colorbar(cmap="rainbow", position="x0c/0c+w4c", frame=True)
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_shading_list():
    """
    Create colorbar and set shading by passing the high/low values as a list.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 2], projection="X10c/2c", frame="a")
    fig.colorbar(cmap="geo", shading=[-0.7, 0.2], frame=True)
    return fig
