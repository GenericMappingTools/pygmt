"""
Test Figure.colorbar.
"""
import pytest
from pygmt import Figure


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_colorbar():
    """
    Create a simple colorbar.
    """
    fig = Figure()
    fig.colorbar(cmap="rainbow", position="x0c/0c+w4c", frame=True)
    return fig
