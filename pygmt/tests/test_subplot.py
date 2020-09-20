"""
Tests subplot
"""
import pytest

from ..pygmtplot import subplots


@pytest.mark.mpl_image_compare
def test_subplot_basic():
    """
    Create a subplot figure with 1 row and 2 columns.
    """
    fig, axs = subplots(nrows=1, ncols=2, figsize=("6c", "3c"))
    fig.sca(ax=axs[0, 0])
    fig.basemap(region=[0, 3, 0, 3], frame=True)
    fig.sca(ax=axs[0, 1])
    fig.basemap(region=[0, 3, 0, 3], frame=True)
    fig.end_subplot()
    return fig


@pytest.mark.mpl_image_compare
def test_subplot_frame():
    """
    Check that map frame setting is applied to all subplot figures
    """
    fig, axs = subplots(nrows=1, ncols=2, figsize=("6c", "3c"), frame="WSne")
    fig.sca(ax=axs[0, 0])
    fig.basemap(region=[0, 3, 0, 3], frame="+tplot0")
    fig.sca(ax=axs[0, 1])
    fig.basemap(region=[0, 3, 0, 3], frame="+tplot1")
    fig.end_subplot()
    return fig


@pytest.mark.mpl_image_compare
def test_subplot_direct():
    """
    Plot map elements to subplots directly using ax argument
    """
    fig, axs = subplots(nrows=2, ncols=1, figsize=("3c", "6c"))
    fig.basemap(region=[0, 3, 0, 3], frame=True, ax=axs[0, 0])
    fig.basemap(region=[0, 3, 0, 3], frame=True, ax=axs[1, 0])
    fig.end_subplot()
    return fig
