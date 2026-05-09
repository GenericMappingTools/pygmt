"""
Test Figure.pygmtlogo.
"""

import pytest
from pygmt import Figure
from pygmt.params import Axis, Position
from pygmt.src.pygmtlogo import _create_logo


@pytest.mark.mpl_image_compare(savefig_kwargs={"dpi": 600})
def test_pygmtlogo_circle_design():
    """
    Test the design details of the PyGMT circular logo.

    This is a regression test to ensure that the design of the logo does not change
    unintentionally. The debugging lines (gridlines and circles) are helpful for
    implementing the logo, but they are not included in the final logo design.
    """
    fig = _create_logo(debug=True)
    return fig


@pytest.mark.mpl_image_compare
def test_pygmtlogo_circle_no_wordmark():
    """
    Test the PyGMT circular logo without the wordmark, including both light/dark themes,
    and colored/black-and-white versions.
    """
    fig = Figure()
    fig.basemap(region=[-0.5, 5.0, -0.5, 5.0], projection="x1c", frame=Axis(grid=0.5))
    fig.pygmtlogo(
        position=Position((1, 3.5), anchor="CM", cstype="mapcoords"),
        theme="light",
    )
    fig.pygmtlogo(
        position=Position((3.5, 3.5), anchor="CM", cstype="mapcoords"),
        theme="dark",
    )
    fig.pygmtlogo(
        position=Position((1, 1), anchor="CM", cstype="mapcoords"),
        theme="light",
        color=False,
    )
    fig.pygmtlogo(
        position=Position((3.5, 1), anchor="CM", cstype="mapcoords"),
        theme="dark",
        color=False,
    )
    return fig
