"""
Tests colorbar
"""
import pytest

from .. import Figure


@pytest.mark.mpl_image_compare
def test_colorbar_using_paper_coordinates():
    """
    Create colorbar positioned at 0cm,0cm with length 1cm and width 0.5cm.
    """
    fig = Figure()
    fig.colorbar(cmap="rainbow", position="x0c/0c+w1c/0.5c")
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_using_paper_coordinates_horizontal():
    """
    Create colorbar positioned at 0cm,0cm with length 2cm oriented horizontally.
    """
    fig = Figure()
    fig.colorbar(cmap="rainbow", position="x0c/0c+w2c+h")
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_positioned_using_map_coordinates():
    """
    Create colorbar positioned at latitude,longitude 3,6 with length 2cm.
    """
    fig = Figure()
    fig.basemap(region=[2, 4, 6, 8], projection="t0/2c", frame=True)
    fig.colorbar(cmap="rainbow", position="g3/6+w2c")
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_positioned_using_justification_code():
    """
    Create colorbar positioned at Top Center inside the map frame with length 2cm.
    """
    fig = Figure()
    fig.basemap(region=[2, 4, 6, 8], projection="t0/2c", frame=True)
    fig.colorbar(cmap="rainbow", position="jTC+w2c")
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_positioned_using_normalized_coords():
    """
    Create colorbar positioned at normalized coordinates 0.75,0.25 with length 2cm.
    """
    fig = Figure()
    fig.basemap(region=[2, 4, 6, 8], projection="t0/2c", frame=True)
    fig.colorbar(cmap="rainbow", position="n0.75/0.25+w2c")
    return fig
