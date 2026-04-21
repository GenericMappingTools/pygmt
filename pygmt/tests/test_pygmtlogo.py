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
def test_pylogo_vertical_wordmark():
    """
    Plot the PyGMT logo with vertical orientation of the wordmark.
    """
    fig = Figure()
    fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=1)
    fig.pygmtlogo(wordmark="vertical")
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
def test_pylogo_color_darkmode():
    """
    Plot the PyGMT logo in dark mode.
    """
    fig = Figure()
    fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=1)
    fig.pygmtlogo(theme="dark")
    return fig


@pytest.mark.mpl_image_compare
def test_pylogo_blackwhite_light():
    """
    Plot the PyGMT logo in dark mode.
    """
    fig = Figure()
    fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=1)
    fig.pygmtlogo(color=False)
    return fig


@pytest.mark.mpl_image_compare
def test_pylogo_backwhite_dark():
    """
    Plot the PyGMT logo in dark mode.
    """
    fig = Figure()
    fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=1)
    fig.pygmtlogo(color=False, theme="dark")
    return fig
