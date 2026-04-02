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


@pytest.mark.mpl_image_compare(filename="test_paragraph_multiple_paragraphs.png")
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
            "This is the first paragraph. \n" * 5
            + "\n"  # Separate the paragraphs with a blank line.
            + "This is the second paragraph. \n" * 5
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


@pytest.mark.mpl_image_compare
def test_paragraph_alignment():
    """
    Test typesetting a single paragraph with different alignments.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 8], projection="X10c/8c", frame=True)
    for x, y, alignment in [
        (5, 1, "left"),
        (5, 3, "right"),
        (5, 5, "center"),
        (5, 7, "justified"),
    ]:
        fig.paragraph(
            x=x,
            y=y,
            text= alignment.upper() + " : " + "This is a long paragraph. " * 5,
            parwidth="8c",
            linespacing="12p",
            alignment=alignment,
        )
    return fig


@pytest.mark.mpl_image_compare
def test_paragraph_font_angle_justify():
    """
    Test typesetting a single paragraph with font, angle, and justify options.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    fig.paragraph(
        x=1,
        y=4,
        text="This is a long paragraph. " * 10,
        parwidth="8c",
        linespacing="12p",
        font="10p,Helvetica-Bold,red",
        angle=45,
        justify="TL",
    )
    return fig
