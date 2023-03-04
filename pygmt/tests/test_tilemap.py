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
    fig.tilemap(region=[-180.0, 180.0, -90, 90], zoom=0, frame="afg")
    return fig
