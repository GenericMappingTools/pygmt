"""
Test Figure.colorbar.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.params.position import Position


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
        fig.colorbar(cmap="gmt/rainbow", position="x0/0", move_text="label")
    with pytest.raises(GMTInvalidInput):
        fig.colorbar(cmap="gmt/rainbow", position="x0/0", label_as_column=True)
