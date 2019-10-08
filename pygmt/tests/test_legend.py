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

    h1 = fig.plot(
        x=[-5],
        y=[5],
        region=[-10, 10, -5, 10],
        projection="X3i/0",
        frame="a",
        style="a15p",
        pen="1.5p,purple",
    )

    h2 = fig.plot(x=[0], y=[5], style="t10p", color="cyan")

    h3 = fig.plot(x=[5], y=[5], style="d5p", color="yellow", pen=True)

    fig.legend(
        [[h1, h2, h3], ["I am a star!", "I am a triangle!", "I am a diamond!"]],
        F=True,
        D="g0/0+w2i+jCM",
    )

    return fig
