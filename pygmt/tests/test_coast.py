"""
Test Figure.coast.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput, GMTParameterError


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_coast_region():
    """
    Test plotting a regional map with coastlines.
    """
    fig = Figure()
    fig.coast(region="JP", projection="M10c", frame=True, land="gray", shorelines=1)
    return fig


@pytest.mark.mpl_image_compare
def test_coast_world_mercator():
    """
    Test generating a global Mercator map with coastlines.
    """
    fig = Figure()
    fig.coast(
        region=[-180, 180, -80, 80],
        projection="M15c",
        frame="af",
        land="#aaaaaa",
        resolution="crude",
        water="white",
    )
    return fig


def test_coast_required_args():
    """
    Test if fig.coast fails when not given required arguments.
    """
    fig = Figure()
    with pytest.raises(GMTParameterError):
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
    Test passing a list of country codes and fill arguments to dcw.
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


@pytest.mark.mpl_image_compare(filename="test_coast_world_mercator.png")
def test_coast_resolution_short_form():
    """
    Test using the short form of the 'resolution' parameter.

    This test is the same as test_coast_world_mercator, but uses the short form of
    the 'resolution' parameter.
    """
    fig = Figure()
    fig.coast(
        region=[-180, 180, -80, 80],
        projection="M15c",
        frame="af",
        land="#aaaaaa",
        D="crude",
        water="white",
    )
    return fig


def test_coast_resolution_long_short_form_conflict():
    """
    Test that using the short form of the 'resolution' parameter conflicts with
    using the long form.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.coast(
            region=[-180, 180, -80, 80],
            projection="M15c",
            frame="af",
            land="#aaaaaa",
            resolution="high",
            D="crude",
            water="white",
        )
