"""
Test Figure.pygmtlogo.
"""

import pytest
from pygmt import Figure


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_pylogo_color_light_nowordmark():
    """
    Plot the PyGMT logo without the wordmark in color using light mode.
    """
    fig = Figure()
    fig.pygmtlogo(wordmark=False)
    return fig


@pytest.mark.mpl_image_compare
def test_pylogo_color_dark_nowordmark():
    """
    Plot the PyGMT logo without the wordmark in color using dark mode.
    """
    fig = Figure()
    fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=1)
    fig.pygmtlogo(wordmark=False, mode="dark")
    return fig
