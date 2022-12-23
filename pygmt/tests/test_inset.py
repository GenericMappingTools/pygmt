"""
Tests for the inset function.
"""
import pytest
from pygmt import Figure


@pytest.mark.mpl_image_compare
def test_inset_aliases():
    """
    Test the aliases for the inset function.
    """
    fig = Figure()
    fig.basemap(region="MG+r2", frame="afg")
    with fig.inset(position="jTL+w3.5c+o0.2c", margin=0, box="+pgreen"):
        fig.basemap(region="g", projection="G47/-20/4c", frame="afg")
    return fig


@pytest.mark.mpl_image_compare
def test_inset_context_manager():
    """
    Test that the inset context manager works and, once closed, plotting
    elements are added to the larger figure.
    """
    fig = Figure()
    fig.basemap(region=[-74, -69.5, 41, 43], projection="M9c", frame=True)
    with fig.inset(position="jBL+w3c+o0.2c", margin=0, box="+pblack"):
        fig.basemap(region=[-80, -65, 35, 50], projection="M3c", frame="afg")
    fig.basemap(rose="jTR+w3c")  # Pass rose argument with basemap after the inset
    return fig
