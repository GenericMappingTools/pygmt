"""
Test Figure.pygmtlogo.
"""

import pytest
from pygmt import Figure


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_pygmtlogo():
    """
    Plot the default PyGMT logo, colored, light theme, without wordmark.
    """
    fig = Figure()
    fig.pygmtlogo()
    return fig


@pytest.mark.mpl_image_compare
def test_pylogo_color_dark_nowordmark():
    """
    Plot the PyGMT logo without wordmark in color using dark mode.
    """
    fig = Figure()
    fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=1)
    fig.pygmtlogo(mode="dark")
    return fig
