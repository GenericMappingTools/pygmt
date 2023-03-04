"""
Tests Figure.tilemap.
"""
import pytest
from pygmt import Figure

contextily = pytest.importorskip("contextily")
rioxarray = pytest.importorskip("rioxarray")


@pytest.mark.mpl_image_compare
def test_tilemap():
    """
    Create a simple tilemap plot.
    """
    fig = Figure()
    fig.tilemap(region=[-157.6, -157.1, 1.68, 2.08], frame="afg")
    return fig
