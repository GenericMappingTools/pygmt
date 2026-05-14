"""
Test Figure.pygmtlogo.
"""

import pytest
from pygmt import Figure
from pygmt.params import Axis, Frame, Position
from pygmt.src.pygmtlogo import _create_logo


@pytest.mark.mpl_image_compare(savefig_kwargs={"dpi": 600})
@pytest.mark.parametrize("wordmark", ["horizontal", "vertical"])
def test_pygmtlogo_circle_design(wordmark):
    """
    Test the design details of the PyGMT circular logo, with a wordmark.

    This is a regression test to ensure that the design of the logo does not change
    unintentionally. The debugging lines (gridlines and circles) are helpful for
    implementing the logo, but they are not included in the final logo design.
    """
    fig = _create_logo(debug=True, wordmark=wordmark)
    return fig


@pytest.mark.mpl_image_compare
def test_pygmtlogo_circle_no_wordmark():
    """
    Test the PyGMT circular logo without the wordmark, including both light/dark themes,
    and colored/black-and-white versions.
    """
    fig = Figure()
    fig.basemap(
        region=[-0.5, 5.0, -0.5, 5.0],
        projection="x1c",
        frame=Frame(fill="gray", axis=Axis(grid=0.5)),
    )
    for (x, y), theme, color in [
        ((1.0, 3.5), "light", True),
        ((3.5, 3.5), "dark", True),
        ((1.0, 1.0), "light", False),
        ((3.5, 1.0), "dark", False),
    ]:
        fig.pygmtlogo(
            position=Position((x, y), anchor="CM", cstype="mapcoords"),
            theme=theme,
            color=color,
        )
    return fig


@pytest.mark.mpl_image_compare
def test_pygmtlogo_circle_horizontal_wordmark():
    """
    Test the PyGMT circular logo with a horizontal wordmark, including both light/dark
    themes, and colored/black-and-white versions.
    """
    fig = Figure()
    fig.basemap(
        region=[-0.5, 8.0, -0.5, 10.0],
        projection="x1c",
        frame=Frame(fill="gray", axis=Axis(grid=0.5)),
    )
    fig.pygmtlogo(
        position=Position((0, 8.5), anchor="ML", cstype="mapcoords"),
        theme="light",
        wordmark="horizontal",
    )
    fig.pygmtlogo(
        position=Position((0, 6), anchor="ML", cstype="mapcoords"),
        theme="dark",
        wordmark="horizontal",
    )
    fig.pygmtlogo(
        position=Position((0, 3.5), anchor="ML", cstype="mapcoords"),
        theme="light",
        color=False,
        wordmark="horizontal",
    )
    fig.pygmtlogo(
        position=Position((0, 1), anchor="ML", cstype="mapcoords"),
        theme="dark",
        color=False,
        wordmark="horizontal",
    )
    return fig
