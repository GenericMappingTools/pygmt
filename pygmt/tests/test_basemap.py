"""
Tests Figure.basemap.
"""
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


def test_basemap_required_args():
    """
    Figure.basemap fails when not given required arguments.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.basemap(region=[10, 70, -3, 8], projection="X8c/6c")


@pytest.mark.mpl_image_compare
def test_basemap():
    """
    Create a simple basemap plot.
    """
    fig = Figure()
    fig.basemap(region=[10, 70, -3, 8], projection="X8c/6c", frame="afg")
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_list_region():
    """
    Create a simple basemap plot passing the region as a list.
    """
    fig = Figure()
    fig.basemap(region=[-20, 50, 200, 500], projection="X6c/6c", frame="a")
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
        frame=['x1p+l"Crustal age"', "y500+lDepth"],
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
