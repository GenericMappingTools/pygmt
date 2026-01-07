"""
Test Figure.colorbar.
"""

import pytest
from pygmt import Figure
from pygmt.alias import AliasSystem
from pygmt.exceptions import GMTInvalidInput
from pygmt.params.position import Position
from pygmt.src.colorbar import _alias_option_D


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_colorbar():
    """
    Create a simple colorbar.
    """
    fig = Figure()
    fig.colorbar(
        cmap="gmt/rainbow",
        position=Position((0, 0), cstype="plotcoords"),
        length=4,
        frame=True,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_shading_list():
    """
    Create colorbar and set shading by passing the high/low values as a list.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 2], projection="X10c/2c", frame="a")
    fig.colorbar(cmap="gmt/geo", shading=[-0.7, 0.2], frame=True)
    return fig


def test_colorbar_alias_D():  # noqa: N802
    """
    Test the parameters for the -D option.
    """

    def alias_wrapper(**kwargs):
        """
        A wrapper function for testing the parameters of -D option.
        """
        return AliasSystem(D=_alias_option_D(**kwargs)).get("D")

    argstr = alias_wrapper(position=Position("TL", offset=0.2), length=4, width=0.5)
    assert argstr == "jTL+o0.2+w4/0.5"

    assert alias_wrapper(orientation="horizontal") == "+h"
    assert alias_wrapper(orientation="vertical") == "+v"

    assert alias_wrapper(reverse=True) == "+r"

    assert alias_wrapper(nan=True) == "+n"
    assert alias_wrapper(nan=True, nan_position="end") == "+N"

    assert alias_wrapper(fg_triangle=True, bg_triangle=True) == "+e"
    assert alias_wrapper(fg_triangle=True) == "+ef"
    assert alias_wrapper(bg_triangle=True) == "+eb"
    argstr = alias_wrapper(fg_triangle=True, bg_triangle=True, triangle_height=0.3)
    assert argstr == "+e0.3"

    assert alias_wrapper(move_text=["annotations", "label", "unit"]) == "+malu"
    assert alias_wrapper(label_as_column=True) == "+mc"

    argstr = alias_wrapper(
        position=Position("BR", offset=(0.1, 0.2)),
        length=5,
        width=0.4,
        orientation="vertical",
        reverse=True,
        nan=True,
        nan_position="start",
        bg_triangle=True,
        triangle_height=0.2,
        move_text=["annotations", "unit"],
        label_as_column=True,
    )
    assert argstr == "jBR+o0.1/0.2+w5/0.4+v+r+n+eb0.2+mauc"


@pytest.mark.mpl_image_compare(filename="test_colorbar.png")
def test_colorbar_position_deprecated_syntax():
    """
    Check that passing the deprecated GMT CLI syntax string to 'position' works.
    """
    fig = Figure()
    fig.colorbar(cmap="gmt/rainbow", position="x0/0+w4c", frame=True)
    return fig


def test_image_position_mixed_syntax():
    """
    Test that mixing deprecated GMT CLI syntax string with new parameters.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.colorbar(cmap="gmt/rainbow", position="x0/0", length="4c")
    with pytest.raises(GMTInvalidInput):
        fig.colorbar(cmap="gmt/rainbow", position="x0/0", width="0.5c")
    with pytest.raises(GMTInvalidInput):
        fig.colorbar(cmap="gmt/rainbow", position="x0/0", orientation="horizontal")
    with pytest.raises(GMTInvalidInput):
        fig.colorbar(cmap="gmt/rainbow", position="x0/0", reverse=True)
    with pytest.raises(GMTInvalidInput):
        fig.colorbar(cmap="gmt/rainbow", position="x0/0", nan=True)
    with pytest.raises(GMTInvalidInput):
        fig.colorbar(
            cmap="gmt/rainbow", position="x0/0", fg_triangle=True, bg_triangle=True
        )
    with pytest.raises(GMTInvalidInput):
        fig.colorbar(cmap="gmt/rainbow", position="x0/0", move_text=["label"])
    with pytest.raises(GMTInvalidInput):
        fig.colorbar(cmap="gmt/rainbow", position="x0/0", label_as_column=True)
