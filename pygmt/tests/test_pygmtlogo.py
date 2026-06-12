"""
Test Figure.pygmtlogo.
"""

import pytest
from pygmt import Figure
from pygmt.params import Axis, Frame, Position
from pygmt.src.pygmtlogo import _create_logo


@pytest.mark.mpl_image_compare(savefig_kwargs={"dpi": 600})
@pytest.mark.parametrize("wordmark", ["horizontal", "vertical"])
@pytest.mark.parametrize("shape", ["circle"])
def test_pygmtlogo_design(shape, wordmark):
    """
    Test the design details of the PyGMT logo with a wordmark.

    This is a regression test to ensure that the design of the logo does not change
    unintentionally. The debugging lines (gridlines and circles) are helpful for
    implementing the logo, but they are not included in the final logo design.
    """
    fig = _create_logo(debug=True, shape=shape, wordmark=wordmark)
    return fig


@pytest.mark.mpl_image_compare
@pytest.mark.parametrize("shape", ["circle"])
def test_pygmtlogo_wordmark_none(shape):
    """
    Test the PyGMT logo without the wordmark, including both light/dark themes, and
    colored/black-and-white versions.
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
            position=Position((x, y), anchor="MC", cstype="mapcoords"),
            theme=theme,
            color=color,
            shape=shape,
        )
    return fig


@pytest.mark.mpl_image_compare
@pytest.mark.parametrize("shape", ["circle"])
def test_pygmtlogo_wordmark_horizontal(shape):
    """
    Test the PyGMT logo with a horizontal wordmark, including both light/dark themes,
    and colored/black-and-white versions.
    """
    fig = Figure()
    fig.basemap(
        region=[-0.5, 8.0, -0.5, 10.0],
        projection="x1c",
        frame=Frame(fill="gray", axis=Axis(grid=0.5)),
    )
    for (x, y), theme, color in [
        ((0, 8.5), "light", True),
        ((0, 6), "dark", True),
        ((0, 3.5), "light", False),
        ((0, 1), "dark", False),
    ]:
        fig.pygmtlogo(
            position=Position((x, y), anchor="ML", cstype="mapcoords"),
            theme=theme,
            color=color,
            shape=shape,
            wordmark="horizontal",
        )
    return fig
