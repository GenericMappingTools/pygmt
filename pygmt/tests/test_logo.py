"""
Tests for fig.logo.
"""
import pytest
from pygmt import Figure


@pytest.mark.mpl_image_compare
def test_logo():
    """
    Plot a GMT logo of a 2 inch width as a stand-alone plot.
    """
    fig = Figure()
    fig.logo(position="x0/0+w2i")
    return fig


@pytest.mark.mpl_image_compare
def test_logo_on_a_map():
    """
    Plot a GMT logo in the upper right corner of a map.
    """
    fig = Figure()
    fig.coast(region=[-90, -70, 0, 20], projection="M6i", land="chocolate", frame=True)
    fig.logo(position="jTR+o0.1i/0.1i+w3i", box=True)
    return fig
