"""
Tests for legend
"""
import pytest

from .. import Figure


@pytest.mark.mpl_image_compare
def test_legend_position():
    """
    Try positioning with each of the four legend coordinate systems.
    """

    fig = Figure()

    fig.basemap(region=[-2, 2, -2, 2], frame=True)

    positions = ["jTR+jTR", "g0/1", "n0.2/0.2", "x4i/2i/2i"]

    for i, position in enumerate(positions):

        fig.plot(x=[0], y=[0], style="p10p", label=i)
        fig.legend(position=position, box=True)

    return fig
