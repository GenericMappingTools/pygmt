"""
Tests ternary.
"""
import pytest
from pygmt import Figure


@pytest.mark.mpl_image_compare
def test_ternary():
    """
    Test plotting a ternary chart.
    """
    fig = Figure()
    fig.ternary(
        data="@ternary.txt",
        region=[0, 100, 0, 100, 0, 100],
        cmap="red,orange,yellow,green,blue,violet",
        width="6i",
        frame=["bafg+lAir", "cafg+lLimestone", "aafg+lWater"],
        style="c0.1c",
        pen="thinnest",
    )
    return fig
