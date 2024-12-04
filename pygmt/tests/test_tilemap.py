"""
Test Figure.tilemap.
"""

import importlib
from unittest.mock import patch

import pytest
from pygmt import Figure

try:
    import contextily

    _HAS_CONTEXTILY = True
except ImportError:
    _HAS_CONTEXTILY = False

_HAS_RIOXARRAY = bool(importlib.util.find_spec("rioxarray"))


@pytest.mark.mpl_image_compare
@pytest.mark.skipif(not _HAS_CONTEXTILY, reason="contextily is not installed")
def test_tilemap_web_mercator():
    """
    Create a tilemap plot in Spherical Mercator projection (EPSG:3857).
    """
    fig = Figure()
    fig.tilemap(
        region=[-20000000.0, 20000000.0, -20000000.0, 20000000.0],
        zoom=0,
        source=contextily.providers.OpenStreetMap.Mapnik,
        lonlat=False,
        frame="afg",
    )
    return fig


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
@pytest.mark.skipif(
    not (_HAS_CONTEXTILY and _HAS_RIOXARRAY),
    reason="contextily and rioxarray are not installed",
)
def test_tilemap_ogc_crs84():
    """
    Create a tilemap plot using longitude/latitude coordinates (OGC:CRS84), centred on
    the international date line.
    """
    fig = Figure()
    fig.tilemap(
        region=[-180.0, 180.0, -90, 90],
        zoom=0,
        source=contextily.providers.OpenStreetMap.Mapnik,
        frame="afg",
        projection="R180/5c",
    )
    return fig


@pytest.mark.mpl_image_compare
@pytest.mark.parametrize("no_clip", [False, True])
@pytest.mark.skipif(
    not (_HAS_CONTEXTILY and _HAS_RIOXARRAY),
    reason="contextily and rioxarray are not installed",
)
def test_tilemap_no_clip(no_clip):
    """
    Create a tilemap plot clipped to the Southern Hemisphere when no_clip is False, but
    for the whole globe when no_clip is True.
    """
    fig = Figure()
    fig.tilemap(
        region=[-180.0, 180.0, -90, 0.6886],
        zoom=0,
        source=contextily.providers.OpenStreetMap.Mapnik,
        frame="afg",
        projection="H180/5c",
        no_clip=no_clip,
    )
    return fig


@pytest.mark.skipif(_HAS_CONTEXTILY, reason="contextily is installed.")
def test_tilemap_no_contextily():
    """
    Raise an ImportError when contextily is not installed.
    """
    fig = Figure()
    with pytest.raises(ImportError, match="Package `contextily` is required"):
        fig.tilemap(
            region=[-20000000.0, 20000000.0, -20000000.0, 20000000.0],
            zoom=0,
            lonlat=False,
            frame="afg",
        )


@pytest.mark.skipif(_HAS_RIOXARRAY, reason="rioxarray is installed.")
def test_tilemap_no_rioxarray():
    """
    Raise an ImportError when rioxarray is not installed and contextily is installed.
    """
    fig = Figure()
    # In our CI, contextily and rioxarray are installed together, so we will see the
    # error about contextily, not rioxarray. Here we mock contextily as installed, to
    # make sure that we see the rioxarray error message when rioxarray is not installed.
    with patch("pygmt.datasets.tile_map._HAS_CONTEXTILY", True):
        with pytest.raises(ImportError, match="Package `rioxarray` is required"):
            fig.tilemap(
                region=[-180.0, 180.0, -90, 90], zoom=0, lonlat=True, frame="afg"
            )
