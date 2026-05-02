"""
Test Figure.pygmtlogo.
"""

import pytest
from pygmt import Figure
from pygmt.params import Axis, Position


@pytest.mark.mpl_image_compare
def test_pygmtlogo_circle_no_wordmark():
    """
    Plot the default PyGMT logo, colored, light and dark themes, without wordmark.
    """
    fig = Figure()
    fig.basemap(region=[-0.5, 5.0, -0.5, 5.0], projection="x1c", frame=Axis(grid=0.5))
    fig.pygmtlogo(
        position=Position((1, 3.5), anchor="CM", cstype="mapcoords"),
        theme="light",
    )
    fig.pygmtlogo(
        position=Position((3.5, 3.5), anchor="CM", cstype="mapcoords"),
        theme="dark",
    )
    return fig
