"""
Tests for legend
"""
import pytest

from .. import Figure


@pytest.mark.mpl_image_compare
def test_legend():
    """
    Create 3-entry legend.
    """
    fig = Figure()

    fig.plot(
        x=[-5],
        y=[5],
        region=[-10, 10, -5, 10],
        projection="X3i/0",
        frame="a",
        style="a15p",
        pen="1.5p,purple",
        label='"I am a star!"',
    )
    fig.plot(x=[0], y=[5], style="t10p", color="cyan", label='"I am a triangle!"')
    fig.plot(
        x=[5], y=[5], style="d5p", color="yellow", pen=True, label='"I am a diamond!"'
    )

    fig.legend(spec="", box=True, position="g0/0+w2i+jCM")
    return fig
