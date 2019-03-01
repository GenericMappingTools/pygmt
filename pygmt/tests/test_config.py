"""
Tests for gmt config
"""
import pytest

from .. import Figure, config


@pytest.mark.mpl_image_compare
def test_config():
    """
    Test if config works globally and locally.
    """
    config(FONT_ANNOT_PRIMARY="blue")
    fig = Figure()
    fig.basemap(
        region="0/10/0/10", projection="X10c/10c", frame=["af", '+t"Blue Annotation"']
    )

    with config(FONT_LABEL="red", FONT_ANNOT_PRIMARY="red"):
        fig.basemap(
            region="0/10/0/10",
            projection="X10c/10c",
            frame=['xaf+l"red label"', "yaf", '+t"red annotation"'],
            X="15c",
        )

    fig.basemap(
        region="0/10/0/10",
        projection="X10c/10c",
        frame=["af", '+t"Blue Annotation"'],
        X="15c",
    )
    return fig
