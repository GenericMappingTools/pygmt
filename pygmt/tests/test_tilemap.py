"""
Test Figure.tilemap.
"""
import pytest
from pygmt import Figure

contextily = pytest.importorskip("contextily")
rioxarray = pytest.importorskip("rioxarray")


@pytest.mark.mpl_image_compare
def test_tilemap_web_mercator():
    """
    Create a tilemap plot in Spherical Mercator projection (EPSG:3857).
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
        region=[-180.0, 180.0, -90, 90], zoom=0, frame="afg", projection="R180/5c"
    )
    return fig


@pytest.mark.mpl_image_compare
@pytest.mark.parametrize("no_clip", [False, True])
def test_tilemap_no_clip(no_clip):
    """
    Create a tilemap plot clipped to the Southern Hemisphere when no_clip is
    False, but for the whole globe when no_clip is True.
    """
    fig = Figure()
    fig.tilemap(
        region=[-180.0, 180.0, -90, 0.6886],
        zoom=0,
        frame="afg",
        projection="H180/5c",
        no_clip=no_clip,
    )
    return fig
