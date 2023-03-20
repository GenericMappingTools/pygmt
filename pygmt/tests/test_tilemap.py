"""
Tests Figure.tilemap.
"""
import pytest
from pygmt import Figure

contextily = pytest.importorskip("contextily")
rioxarray = pytest.importorskip("rioxarray")


@pytest.mark.mpl_image_compare
def test_tilemap_web_mercator():
    """
    Create a tilemap plot in Web Mercator projection (EPSG:3857).
    """
    fig = Figure()
    fig.tilemap(
        region=[-20000000.0, 20000000.0, -20000000.0, 20000000.0],
        zoom=0,
        lonlat=False,
        frame="afg",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_tilemap_ogc_wgs84():
    """
    Create a tilemap plot using longitude/latitude coordinates (OGC:WGS84),
    centred on the international date line.
    """
    fig = Figure()
    fig.tilemap(
        region=[-180.0, 180.0, -90, 90],
        zoom=0,
        frame="afg",
        projection="R180/5c",
        verbose=True,
    )
    return fig
