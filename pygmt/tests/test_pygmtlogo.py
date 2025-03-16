"""
Test Figure.pygmtlogo.
"""

import pytest
from pygmt import Figure


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_pylogo():
    """
    Plot the PyGMT logo as a stand-alone plot.
    """
    fig = Figure()
    fig.pygmtlogo()
    return fig


@pytest.mark.mpl_image_compare
def test_pylogo_on_a_map():
    """
    Plot the PyGMT logo at the lower right corner of a map.
    """
    fig = Figure()
    fig.basemap(region=[-90, -70, 0, 20], projection="M15c", frame=True)
    fig.pygmtlogo(position="jBR+o0.25c/0.25c+w7.5c", box=True)
    return fig
