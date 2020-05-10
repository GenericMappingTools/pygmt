"""
Tests subplot
"""
import pytest

from .. import Figure
from ..exceptions import GMTInvalidInput


@pytest.mark.mpl_image_compare
def test_subplot_basic():
    """
    Create a subplot figure with 1 row and 2 columns.
    """
    fig = Figure()
    fig.subplot(directive="begin", row=1, col=2, dimensions="f6c/3c")
    fig.subplot(directive="set", row=0, col=0)
    fig.basemap(region=[0, 3, 0, 3], frame=True)
    fig.subplot(directive="set", row=0, col=1)
    fig.basemap(region=[0, 3, 0, 3], frame=True)
    fig.subplot(directive="end")
    return fig


@pytest.mark.mpl_image_compare
def test_subplot_frame():
    """
    Check that map frame setting is applied to all subplot figures
    """
    fig = Figure()
    fig.subplot(directive="begin", row=1, col=2, dimensions="f6c/3c", frame="WSne")
    fig.subplot(directive="set", row=0, col=0)
    fig.basemap(region=[0, 3, 0, 3], frame="+tplot0")
    fig.subplot(directive="set", row=0, col=1)
    fig.basemap(region=[0, 3, 0, 3], frame="+tplot1")
    fig.subplot(directive="end")
    return fig


def test_subplot_incorrect_directive():
    """
    Check that subplot fails when an incorrect directive is used
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.subplot(directive="start")
