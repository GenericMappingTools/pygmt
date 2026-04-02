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
@pytest.mark.parametrize("inputtype", ["list", "string"])
def test_paragraph_multiple_paragraphs(inputtype):
    """
    Test typesetting multiple paragraphs.
    """
    if inputtype == "list":
        text = [
            "This is the first paragraph. " * 5,
            "This is the second paragraph. " * 5,
        ]
    else:
        text = (
            "This is the first paragraph.\n" * 5
            + "\n\n"
            + "This is the second paragraph.\n" * 5
        )

    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    fig.paragraph(
        x=4,
        y=4,
        text=text,
        parwidth="5c",
        linespacing="12p",
    )
    return fig
