"""
Tests for fig.coast.
"""
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


@pytest.mark.mpl_image_compare
def test_coast_iceland():
    """
    Test passing in region as a list.
    """
    fig = Figure()
    fig.coast(region=[-30, -10, 60, 65], projection="m1c", frame=True, land="p28+r100")
    return fig


@pytest.mark.mpl_image_compare
def test_coast_world_mercator():
    """
    Test passing generating a global Mercator map with coastlines.
    """
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


def test_coast_required_args():
    """
    Test if fig.coast fails when not given required arguments.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.coast(region="EG")


@pytest.mark.mpl_image_compare
def test_coast_dcw_single():
    """
    Test passing a single country code to dcw.
    """
    fig = Figure()
    fig.coast(
        region=[-10, 15, 25, 44],
        frame="a",
        projection="M15c",
        land="brown",
        dcw="ES+gbisque+pblue",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_coast_dcw_list():
    """
    Test passing a list of country codes and fill options to dcw.
    """
    fig = Figure()
    fig.coast(
        region=[-10, 15, 25, 44],
        frame="a",
        projection="M15c",
        land="brown",
        dcw=["ES+gbisque+pgreen", "IT+gcyan+pblue"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_coast_dcw_continent():
    """
    Test passing a continent code to dcw.
    """
    fig = Figure()
    fig.coast(
        region=[-10, 15, 25, 44],
        frame="a",
        projection="M15c",
        land="brown",
        dcw="=AF+gbisque+pblue",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_coast_dcw_state():
    """
    Test passing a US state code to dcw.
    """
    fig = Figure()
    fig.coast(
        region=[-75, -69, 40, 44],
        frame="a",
        projection="M15c",
        land="brown",
        dcw="US.MA+gbisque+pblue",
    )
    return fig
