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
    text = [
        "  Paragraph 1: Two leading whitespaces. Three inline   whitespaces. Two trailing whitespaces.  ",
        "	Paragraph 2: One leading tab results in one indentation (four whitespaces by default).",
        "		Paragraph 3: Two leading tabs results in two indentation (eight whitespaces by default).",
        "Paragraph 4: Multiple inline			tabs are converted to multiple spaces. Trailing tabs have not effects.		",
        "Paragraph 5: Mixing tabs and spaces. 2T3STST(		   	 	).",
        "\nParagraph 6: Leading newline is converted to a space. Trailing newlines are converted to spaces.\n\n",
        "\n\nParagraph 7: Multiple leading newline are converted to multiple spaces. xxx yyy zzz.",
        "Paragraph 8: Newlines insiden a paragraph\nare converted to spaces.",
        "Paragraph 9: This is the last paragraph.",
    ]
    if inputtype == "string":
        text = "\n\n".join(text)

    fig = Figure()
    fig.basemap(region=[0, 17, 0, 8], projection="x1c", frame=True)
    fig.paragraph(
        x=1,
        y=1,
        text=text,
        font="Courier",
        justify="BL",
        parwidth="15c",
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
            text=alignment.upper() + " : " + "This is a long paragraph. " * 5,
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


@pytest.mark.mpl_image_compare
def test_paragraph_blank_line():
    """
    Test typesetting a single paragraph with blank_line option.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 4], projection="X10c/4c", frame=True)
    text = (
        "This is a long paragraph. " * 5
        + "\n\n"
        + "This is another long paragraph. " * 5
    )
    fig.paragraph(
        x=5, y=2, text=text, parwidth="8c", linespacing="12p", blank_line=True
    )
    return fig


@pytest.mark.mpl_image_compare
def test_paragraph_tab_width():
    """
    Test typesetting a single paragraph with tab_width option.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 4], projection="X10c/6c", frame=True)
    text = "A paragraph with tabs\tinside. " * 3
    fig.paragraph(x=5, y=3, text=text, parwidth="8c", linespacing="12p")
    fig.paragraph(x=5, y=2, text=text, parwidth="8c", linespacing="12p", tab_width=0)
    fig.paragraph(x=5, y=1, text=text, parwidth="8c", linespacing="12p", tab_width=8)
    return fig
