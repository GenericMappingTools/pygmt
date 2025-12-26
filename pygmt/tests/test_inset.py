"""
Test Figure.inset.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.params import Box, Position


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_inset_aliases():
    """
    Test the aliases for the inset function.
    """
    fig = Figure()
    fig.basemap(region="MG+r2", frame="afg")
    with fig.inset(
        position=Position("TL", offset=0.2),
        width="3.5c",
        clearance=0.2,
        box=Box(pen="green"),
    ):
        fig.basemap(region="g", projection="G47/-20/?", frame="afg")
    return fig


@pytest.mark.mpl_image_compare
def test_inset_context_manager():
    """
    Test that the inset context manager works and, once closed, plotting elements are
    added to the larger figure.
    """
    fig = Figure()
    fig.basemap(region=[-74, -69.5, 41, 43], projection="M9c", frame=True)
    with fig.inset(
        position=Position("BL", offset=0.2), width="3c", clearance=0.2, box=True
    ):
        fig.basemap(region="g", projection="G47/-20/?", frame="afg")
    # Plot an rose after the inset
    fig.directional_rose(position="TR", width="3c")
    return fig


@pytest.mark.mpl_image_compare
def test_inset_default_position():
    """
    Test that the inset defaults to the bottom-left corner when no position is given.
    """
    fig = Figure()
    fig.basemap(region="MG+r2", frame="afg")
    with fig.inset(width="3.5c", box=True):
        fig.basemap(region="g", projection="G47/-20/?", frame="afg")
    return fig


@pytest.mark.mpl_image_compare(filename="test_inset_default_position.png")
def test_inset_width_from_projection_region():
    """
    Test that the inset can infer width from projection and region.
    """
    fig = Figure()
    fig.basemap(region="MG+r2", frame="afg")
    with fig.inset(projection="G47/-20/3.5c", region="g", box=True):
        fig.basemap(region="g", projection="G47/-20/?", frame="afg")
    return fig


@pytest.mark.mpl_image_compare(filename="test_inset_aliases.png")
def test_inset_deprecated_position():
    """
    Test that the deprecated raw GMT CLI string for position still works.
    """
    fig = Figure()
    fig.basemap(region="MG+r2", frame="afg")
    with fig.inset(position="jTL+w3.5c+o0.2c", clearance=0.2, box=Box(pen="green")):
        fig.basemap(region="g", projection="G47/-20/?", frame="afg")
    return fig


def test_inset_invalid_inputs():
    """
    Test that an error is raised when invalid inputs are provided.
    """
    fig = Figure()
    fig.basemap(region="MG+r2", frame="afg")
    # Width is not given
    with pytest.raises(GMTInvalidInput):
        with fig.inset(position=Position("TL")):
            pass
    # Height is given but width is not given
    with pytest.raises(GMTInvalidInput):
        with fig.inset(position=Position("TL"), height="5c"):
            pass
    # Old position syntax conflicts with width/height
    with pytest.raises(GMTInvalidInput):
        with fig.inset(position="jTL+w3.5c", width="3.5c"):
            pass
