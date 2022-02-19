"""
Tests for fig.coast.
"""
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


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
        resolution="c",
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
def test_coast_clip_land():
    """
    Test to clip dry areas.
    """
    region = [-28, -10, 62, 68]

    fig = Figure()
    fig.basemap(region=region, projection="M8c", frame=True)
    fig.coast(resolution="l", clip="land")
    fig.plot(
        x=[-22.5, -22.5, -15, -15],
        y=[66, 64, 66, 64],
        style="c4c",
        color="red",
        pen="1.5p,black",
    )
    fig.coast(clip="end")
    return fig


@pytest.mark.mpl_image_compare
def test_coast_clip_water():
    """
    Test to clip wet areas.
    """
    region = [-28, -10, 62, 68]

    fig = Figure()
    fig.basemap(region=region, projection="M8c", frame=True)
    fig.coast(resolution="l", clip="water")
    fig.plot(
        x=[-22.5, -22.5, -15, -15],
        y=[66, 64, 66, 64],
        style="c4c",
        color="red",
        pen="1.5p,black",
    )
    fig.coast(clip="end")
    return fig


def test_coast_fail_invalid_parameter():
    """
    Coast should raise an exception if an invalid parameter is given as input.
    """
    region = [-28, -10, 62, 68]

    fig = Figure()

    with pytest.raises(GMTInvalidInput):
        fig.coast(region=region, resolution="l", clip="invalid")
