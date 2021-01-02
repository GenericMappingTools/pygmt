"""
Tests for coast
"""
import pytest
from pygmt import Figure
from pygmt.helpers.testing import check_figures_equal


@pytest.mark.mpl_image_compare
def test_coast():
    "Simple plot from the GMT docs"
    fig = Figure()
    fig.coast(
        R="-30/30/-40/40",
        J="m0.1i",
        B=5,
        I="1/1p,blue",
        N="1/0.25p,-",
        W="0.25p,white",
        G="green",
        S="blue",
        D="c",
        A=10000,
    )
    return fig


@check_figures_equal()
def test_coast_iceland():
    "Test passing in R as a list"
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.coast(R="-30/-10/60/65", J="m1c", B="", G="p28+r100")
    fig_test.coast(
        region=[-30, -10, 60, 65], projection="m1c", frame=True, land="p28+r100"
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_coast_aliases():
    "Test that all aliases work"
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.coast(
        R="-30/30/-40/40",
        J="M25c",
        B="afg",
        I="1/1p,black",
        N="1/0.5p,-",
        W="0.25p,white",
        G="moccasin",
        S="skyblue",
        D="i",
        A=1000,
        L="jCM+c1+w1000k+f+l",
        U=True,
        X="a4c",
        Y="a10c",
        p="135/25",
        t=13,
        C="blue"
    )
    fig_test.coast(
        region=[-30, 30, -40, 40],  # R
        projection="M25c",  # J
        frame="afg",  # B
        rivers="1/1p,black",  # I
        borders="1/0.5p,-",  # N
        shorelines="0.25p,white",  # W
        land="moccasin",  # G
        water="skyblue",  # S
        resolution="i",  # D
        area_thresh=1000,  # A
        map_scale="jCM+c1+w1000k+f+l",  # L
        timestamp=True,  # U
        xshift="a4c",  # X
        yshift="a10c",  # Y
        perspective=[135, 25],  # p
        transparency=13,  # t
        lakes="blue" # C
    )
    return fig_ref, fig_test


@pytest.mark.mpl_image_compare
def test_coast_world_mercator():
    "Test passing generating a global Mercator map with coastlines"
    fig = Figure()
    fig.coast(
        region=[-180, 180, -80, 80],
        projection="M10i",
        frame="af",
        land="#aaaaaa",
        resolution="l",
        water="white",
    )
    return fig
