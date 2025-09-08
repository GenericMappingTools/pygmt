"""
Test Figure.inset.
"""

import pytest
from pygmt import Figure
from pygmt.params import Box


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_inset_aliases():
    """
    Test the aliases for the inset function.
    """
    fig = Figure()
    fig.basemap(region="MG+r2", frame="afg")
    with fig.inset(position="jTL+w3.5c+o0.2c", clearance=0.2, box=Box(pen="green")):
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
    with fig.inset(position="jBL+w3c+o0.2c", clearance=0.2, box=True):
        fig.basemap(region="g", projection="G47/-20/?", frame="afg")
    # Plot an rose after the inset
    fig.directional_rose(position="TR", width="3c")
    return fig
