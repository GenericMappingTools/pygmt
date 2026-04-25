"""
Test Figure.pygmtlogo.
"""

import pytest
from pygmt import Figure


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_pygmtlogo():
    """
    Plot the default PyGMT logo, colored, light and dark themes, without wordmark.
    """
    fig = Figure()
    fig.pygmtlogo()
    fig.shift_origin(xshift="+w")
    fig.pygmtlogo(mode="dark")
    return fig
