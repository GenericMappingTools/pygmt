"""
Tests ternary.
"""
import pytest
from pygmt import Figure, makecpt


@pytest.mark.mpl_image_compare
def test_ternary():
    """
    Test plotting a ternary chart.
    """
    fig = Figure()
    fig.ternary(
        table="@ternary.txt",
        region="0/100/0/100/0/100",
        cmap="red,orange,yellow,green,blue,violet",
        projection="6i",
        frame=["bafg+lAir", "cafg+lLimestone", "aafg+lWater"],
        style="c0.1c",
    )
    return fig
