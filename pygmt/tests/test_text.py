# pylint: disable=redefined-outer-name
"""
Tests text.
"""
import os

import numpy as np
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTCLibError, GMTInvalidInput
from pygmt.helpers import GMTTempFile

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")
CITIES_DATA = os.path.join(TEST_DATA_DIR, "cities.txt")


@pytest.fixture(scope="module")
def projection():
    """
    The projection system.
    """
    return "x10c"


@pytest.fixture(scope="module")
def region():
    """
    The data region.
    """
    return [0, 5, 0, 2.5]


@pytest.mark.mpl_image_compare
def test_text_single_line_of_text(region, projection):
    """
    Place a single line text of text at some x, y location.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=2.4,
        text="This is a line of text",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_multiple_lines_of_text(region, projection):
    """
    Place multiple lines of text at their respective x, y locations.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=[1.2, 1.6],
        y=[0.6, 0.3],
        text=["This is a line of text", "This is another line of text"],
    )
    return fig


def test_text_without_text_input(region, projection):
    """
    Run text by passing in x and y, but no text.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.text(region=region, projection=projection, x=1.2, y=2.4)


@pytest.mark.mpl_image_compare
def test_text_input_single_filename():
    """
    Run text by passing in one filename to textfiles.
    """
    fig = Figure()
    fig.text(region=[10, 70, -5, 10], textfiles=POINTS_DATA)
    return fig


@pytest.mark.mpl_image_compare
def test_text_input_remote_filename():
    """
    Run text by passing in a remote filename to textfiles.
    """
    fig = Figure()
    fig.text(region=[0, 6.5, 0, 6.5], textfiles="@Table_5_11.txt")
    return fig


@pytest.mark.mpl_image_compare
def test_text_input_multiple_filenames():
    """
    Run text by passing in multiple filenames to textfiles.
    """
    fig = Figure()
    fig.text(region=[10, 70, -30, 10], textfiles=[POINTS_DATA, CITIES_DATA])
    return fig


def test_text_nonexistent_filename():
    """
    Run text by passing in a list of filenames with one that does not exist.
    """
    fig = Figure()
    with pytest.raises(GMTCLibError):
        fig.text(region=[10, 70, -5, 10], textfiles=[POINTS_DATA, "notexist.txt"])


@pytest.mark.mpl_image_compare
def test_text_position(region):
    """
    Print text at center middle (CM) and eight other positions
    (Top/Middle/Bottom x Left/Centre/Right).
    """
    fig = Figure()
    fig.text(region=region, projection="x1c", frame="a", position="CM", text="C M")
    for position in ("TL", "TC", "TR", "ML", "MR", "BL", "BC", "BR"):
        fig.text(position=position, text=position)
    return fig


def test_text_xy_with_position_fails(region):
    """
    Run text by providing both x/y pairs and position arguments.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.text(
            region=region, projection="x1c", x=1.2, y=2.4, position="MC", text="text"
        )


@pytest.mark.mpl_image_compare
def test_text_position_offset_with_line(region):
    """
    Print text at centre middle (CM) and eight other positions
    (Top/Middle/Bottom x Left/Centre/Right), offset by 0.5 cm, with a line
    drawn from the original to the shifted point.
    """
    fig = Figure()
    fig.text(region=region, projection="x1c", frame="a", position="CM", text="C M")
    for position in ("TL", "TC", "TR", "ML", "MR", "BL", "BC", "BR"):
        fig.text(position=position, text=position, offset="j0.5c+v")
    return fig


@pytest.mark.mpl_image_compare
def test_text_angle_30(region, projection):
    """
    Print text at 30 degrees counter-clockwise from horizontal.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=2.4,
        text="text angle 30 degrees",
        angle=30,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_font_bold(region, projection):
    """
    Print text with a bold font.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=2.4,
        text="text in bold",
        font="Helvetica-Bold",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_fill(region, projection):
    """
    Print text with blue color fill.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=1.2,
        text="blue fill around text",
        fill="blue",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_pen(region, projection):
    """
    Print text with thick green dashed pen.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=1.2,
        text="green pen around text",
        pen="thick,green,dashed",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_round_clearance(region, projection):
    """
    Print text with round rectangle box clearance.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=1.2,
        text="clearance around text",
        clearance="90%+tO",
        pen="default,black,dashed",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_justify_bottom_right_and_top_left(region, projection):
    """
    Print text justified at bottom right and top left.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=0.2,
        text="text justified bottom right",
        justify="BR",
    )
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=0.2,
        text="text justified top left",
        justify="TL",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_justify_parsed_from_textfile():
    """
    Print text justified based on a column from textfile, using justify=True
    boolean operation.

    Loosely based on "All great-circle paths lead to Rome"
    gallery example at
    https://gmt.soest.hawaii.edu/doc/latest/gallery/ex23.html
    """
    fig = Figure()
    fig.text(
        region="g",
        projection="H90/9i",
        justify=True,
        textfiles=CITIES_DATA,
        D="j0.45/0+vred",  # draw red-line from xy point to text label (city name)
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_angle_font_justify_from_textfile():
    """
    Print text with x, y, angle, font, justify, and text arguments parsed from
    the textfile.
    """
    fig = Figure()
    with GMTTempFile(suffix=".txt") as tempfile:
        with open(tempfile.name, "w") as tmpfile:
            tmpfile.write("114 0.5 30 22p,Helvetica-Bold,black LM BORNEO")
        fig.text(
            region=[113, 117.5, -0.5, 3],
            projection="M5c",
            frame="a",
            textfiles=tempfile.name,
            angle=True,
            font=True,
            justify=True,
        )
    return fig


@pytest.mark.mpl_image_compare
def test_text_transparency():
    """
    Add texts with a constant transparency.
    """
    x = np.arange(1, 10)
    y = np.arange(11, 20)
    text = [f"TEXT-{i}-{j}" for i, j in zip(x, y)]

    fig = Figure()

    fig.basemap(region=[0, 10, 10, 20], projection="X10c", frame=True)
    fig.text(x=x, y=y, text=text, transparency=50)

    return fig


@pytest.mark.mpl_image_compare
def test_text_varying_transparency():
    """
    Add texts with varying transparency.
    """
    x = np.arange(1, 10)
    y = np.arange(11, 20)
    text = [f"TEXT-{i}-{j}" for i, j in zip(x, y)]
    transparency = np.arange(10, 100, 10)

    fig = Figure()
    fig.basemap(region=[0, 10, 10, 20], projection="X10c", frame=True)
    fig.text(x=x, y=y, text=text, transparency=transparency)

    return fig


@pytest.mark.mpl_image_compare
def test_text_nonstr_text():
    """
    Input text is in non-string type (e.g., int, float)
    """
    fig = Figure()

    fig.text(
        region=[0, 10, 0, 10],
        projection="X10c",
        frame=True,
        x=[1, 2, 3, 4],
        y=[1, 2, 3, 4],
        text=[1, 2, 3.0, 4.0],
    )

    return fig
