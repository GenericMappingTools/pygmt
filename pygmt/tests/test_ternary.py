"""
Tests for pygmt.ternary.
"""
import pytest
from pygmt import Figure, makecpt

@pytest.mark.mpl_image_compare
def test_ternary():
    """
    Test plotting a ternary chart.
    """
    fig = Figure()
    makecpt(cmap="turbo", series=[0, 80, 10])
    fig.ternary(table="@ternary.txt",
                region="0/100/0/100/0/100",
                cmap=True,
                projection="X6i",
                frame=["bafg+lAir",
                       "cafg+lLimestone",
                       "aafg+lWater"],
                style="c0.1c")
    return fig
