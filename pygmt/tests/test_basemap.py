"""
Tests fig.basemap.
"""
import pytest

from .. import Figure
from ..exceptions import GMTInvalidInput


def test_basemap_required_args():
    "fig.basemap fails when not given required arguments"
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.basemap(R="10/70/-3/8", J="X4i/3i")


@pytest.mark.mpl_image_compare
def test_basemap():
    "Create a simple basemap plot"
    fig = Figure()
    fig.basemap(R="10/70/-3/8", J="X4i/3i", B="afg")
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_list_region():
    "Create a simple basemap plot passing the region as a list"
    fig = Figure()
    fig.basemap(R=[-20, 50, 200, 500], J="X3i/3i", B="a")
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_loglog():
    "Create a loglog basemap plot"
    fig = Figure()
    fig.basemap(
        R="1/10000/1e20/1e25",
        J="X25cl/15cl",
        Bx="2+lWavelength",
        By="a1pf3+lPower",
        B="WS",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_power_axis():
    "Create a power axis basemap plot"
    fig = Figure()
    fig.basemap(
        R=[0, 100, 0, 5000], J="x1p0.5/-0.001", B=['x1p+l"Crustal age"', "y500+lDepth"]
    )
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_polar():
    "Create a polar basemap plot"
    fig = Figure()
    fig.basemap(R="0/360/0/1000", J="P6i", B="afg")
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_winkel_tripel():
    "Create a Winkel Tripel basemap plot"
    fig = Figure()
    fig.basemap(R="90/450/-90/90", J="R270/25c", B="afg")
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_aliases():
    "Make sure the argument aliases work"
    fig = Figure()
    fig.basemap(region=[0, 360, -90, 90], projection="W7i", frame=True)
    return fig
