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


@pytest.mark.mpl_image_compare
def test_legend_entries():
    """
    Test different marker types/shapes.
    """

    fig = Figure()

    fig.basemap(projection="x1i", region=[0, 7, 3, 7], frame=True)

    fig.plot(
        data="@Table_5_11.txt",
        style="c0.15i",
        color="lightgreen",
        pen="faint",
        l="Apples",
    )
    fig.plot(data="@Table_5_11.txt", pen="1.5p,gray", l='"My lines"')
    fig.plot(data="@Table_5_11.txt", style="t0.15i", color="orange", l="Oranges")

    fig.legend(position="JTR+jTR")

    return fig
