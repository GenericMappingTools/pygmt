"""
Tests fig.basemap.
"""
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.testing import check_figures_equal


def test_basemap_required_args():
    """
    fig.basemap fails when not given required arguments.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.basemap(R="10/70/-3/8", J="X4i/3i")


@pytest.mark.mpl_image_compare
def test_basemap():
    """
    Create a simple basemap plot.
    """
    fig = Figure()
    fig.basemap(R="10/70/-3/8", J="X4i/3i", B="afg")
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_list_region():
    """
    Create a simple basemap plot passing the region as a list.
    """
    fig = Figure()
    fig.basemap(R=[-20, 50, 200, 500], J="X3i/3i", B="a")
    return fig


@pytest.mark.mpl_image_compare
def test_basemap_loglog():
    """
    Create a loglog basemap plot.
    """
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
    """
    Create a power axis basemap plot.
    """
    fig = Figure()
    fig.basemap(
        R=[0, 100, 0, 5000], J="x1p0.5/-0.001", B=['x1p+l"Crustal age"', "y500+lDepth"]
    )
    return fig


@check_figures_equal()
def test_basemap_polar():
    """
    Create a polar basemap plot.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.basemap(R="0/360/0/1000", J="P6i", B="afg")
    fig_test.basemap(region=[0, 360, 0, 1000], projection="P6i", frame="afg")

    return fig_ref, fig_test


@check_figures_equal()
def test_basemap_winkel_tripel():
    """
    Create a Winkel Tripel basemap plot.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.basemap(R="90/450/-90/90", J="R270/25c", B="afg")
    fig_test.basemap(region=[90, 450, -90, 90], projection="R270/25c", frame="afg")
    return fig_ref, fig_test


@check_figures_equal()
def test_basemap_rose():
    """
    Create a map with coast and use basemap to add a rose.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.coast(R="127.5/128.5/26/27", W="1/0.5p")
    fig_ref.basemap(Td="jBR+w5c")
    fig_test.coast(region=[127.5, 128.5, 26, 27], shorelines="1/0.5p")
    fig_test.basemap(rose="jBR+w5c")
    return fig_ref, fig_test


@check_figures_equal()
def test_basemap_compass():
    """
    Create a map with coast and use basemap to add a compass.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.coast(R="127.5/128.5/26/27", W="1/0.5p")
    fig_ref.basemap(Tm="jBR+w5c+d11.5")
    fig_test.coast(region=[127.5, 128.5, 26, 27], shorelines="1/0.5p")
    fig_test.basemap(compass="jBR+w5c+d11.5")
    return fig_ref, fig_test


@check_figures_equal()
def test_basemap_map_scale():
    """
    Create a map with coast and use basemap to add a map scale.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.coast(R="127.5/128.5/26/27", W="1/0.5p")
    fig_ref.basemap(L="jMB+c1+w10k+l+f")
    fig_test.coast(region=[127.5, 128.5, 26, 27], shorelines="1/0.5p")
    fig_test.basemap(map_scale="jMB+c1+w10k+f+l")
    return fig_ref, fig_test
