"""
Test Figure.pygmtlogo.
"""

import pytest
from pygmt import Figure


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_pylogo():
    """
    Plot the PyGMT logo using the default settings.
    """
    fig = Figure()
    fig.pygmtlogo()
    return fig


@pytest.mark.mpl_image_compare
def test_pylogo_on_a_map():
    """
    Plot the PyGMT logo and adjust the position, offset, and size.
    """
    fig = Figure()
    fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=1)
    fig.pygmtlogo(position="jMC+o0.25c/0.25c+w7.5c", box=True)
    return fig


@pytest.mark.mpl_image_compare
def test_pylogo_no_wordmark():
    """
    Plot the PyGMT logo without wordmark.
    """
    fig = Figure()
    fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=1)
    fig.pygmtlogo(wordmark=False)
    return fig


@pytest.mark.mpl_image_compare
def test_pylogo_lightmode():
    """
    Plot the PyGMT logo in dark mode.
    """
    fig = Figure()
    fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=1)
    fig.pygmtlogo(theme="dark")
    return fig


@pytest.mark.mpl_image_compare
def test_pylogo_vertical():
    """
    Plot the PyGMT logo with vertical orientation of the wordmark.
    """
    fig = Figure()
    fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=1)
    fig.pygmtlogo(wordmark="vertical")
    return fig
