"""
Tests Figure.basemap.
"""
import pytest
from pygmt import Figure


@pytest.mark.mpl_image_compare
def test_basemap_required_args():
    """
    Automatically set `frame=True` when required arguments are not given.
    """
    fig = Figure()
    fig.basemap(region=[10, 70, -3, 8], projection="X8c/6c")
    return fig


@pytest.mark.mpl_image_compare
def test_basemap():
    """
    Create a simple basemap plot.
    """
    fig = Figure()
    fig.basemap(region=[10, 70, -3, 8], projection="X8c/6c", frame="afg")
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_loglog():
    """
    Create a loglog basemap plot.
    """
    fig = Figure()
    fig.basemap(
        region=[1, 10000, 1e20, 1e25],
        projection="X16cl/12cl",
        frame=["WS", "x2+lWavelength", "ya1pf3+lPower"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_power_axis():
    """
    Create a power axis basemap plot.
    """
    fig = Figure()
    fig.basemap(
        region=[0, 100, 0, 5000],
        projection="x1p0.5/-0.001",
        frame=["x1p+lCrustal age", "y500+lDepth"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_polar():
    """
    Create a polar basemap plot.
    """
    fig = Figure()
    fig.basemap(region=[0, 360, 0, 1000], projection="P8c", frame="afg")
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_winkel_tripel():
    """
    Create a Winkel Tripel basemap plot.
    """
    fig = Figure()
    fig.basemap(region=[90, 450, -90, 90], projection="R270/20c", frame="afg")
    return fig


@pytest.mark.mpl_image_compare(filename="test_basemap_utm_projection.png")
@pytest.mark.parametrize(
    "projection",
    [
        "EPSG_32723 +width=5",
        "+proj=utm +zone=23 +south +datum=WGS84 +units=m +no_defs +width=5",
    ],
)
def test_basemap_utm_projection(projection):
    """
    Create a Universal Transverse Mercator (Zone 23S) basemap plot.

    Also check that providing the projection as an EPSG code or PROJ4 string
    works.
    """
    projection = projection.replace(
        "EPSG_", "EPSG:"  # workaround Windows not allowing colons in filenames
    )
    fig = Figure()
    fig.basemap(region=[-52, -50, -12, -11], projection=projection, frame="afg")
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_rose():
    """
    Create a map with a rose.
    """
    fig = Figure()
    fig.basemap(
        region=[127.5, 128.5, 26, 27], projection="H15c", frame=True, rose="jMC+w5c"
    )
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_compass():
    """
    Create a map with a compass.
    """
    fig = Figure()
    fig.basemap(
        region=[127.5, 128.5, 26, 27],
        projection="H15c",
        frame=True,
        compass="jMC+w5c+d11.5",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_map_scale():
    """
    Create a map with a map scale.
    """
    fig = Figure()
    fig.basemap(
        region=[127.5, 128.5, 26, 27],
        projection="H15c",
        frame=True,
        map_scale="jMC+c26.5+w10k+f+l",
    )
    return fig
