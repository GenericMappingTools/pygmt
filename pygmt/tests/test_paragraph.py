"""
Tests for Figure.paragraph.
"""

import pytest
from pygmt import Figure


@pytest.mark.mpl_image_compare
def test_paragraph():
    """
    Test typesetting a single paragraph.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    fig.paragraph(
        x=4,
        y=4,
        text="This is a long paragraph. " * 10,
        parwidth="5c",
        linespacing="12p",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_paragraph_multiple_paragraphs_list():
    """
    Test typesetting a single paragraph.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    fig.paragraph(
        x=4,
        y=4,
        text=[
            "This is the first paragraph. " * 5,
            "This is the second paragraph. " * 5,
        ],
        parwidth="5c",
        linespacing="12p",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_paragraph_multiple_paragraphs_blankline():
    """
    Test typesetting a single paragraph.
    """
    text = """
This is the first paragraph.
This is the first paragraph.
This is the first paragraph.
This is the first paragraph.
This is the first paragraph.

This is the second paragraph.
This is the second paragraph.
This is the second paragraph.
This is the second paragraph.
This is the second paragraph.
"""
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    fig.paragraph(x=4, y=4, text=text, parwidth="5c", linespacing="12p")
    return fig
