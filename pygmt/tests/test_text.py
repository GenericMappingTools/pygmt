# pylint: disable=redefined-outer-name
"""
Tests text
"""
import os

import pytest

from .. import Figure
from ..exceptions import GMTInvalidInput

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")
CITIES_DATA = os.path.join(TEST_DATA_DIR, "cities.txt")


@pytest.fixture(scope="module")
def projection():
    "The projection system"
    return "x4i"


@pytest.fixture(scope="module")
def region():
    "The data region"
    return [0, 5, 0, 2.5]


@pytest.mark.mpl_image_compare
def test_text_single_line_of_text(region, projection):
    """
    Place a single line text of text at some x, y location
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
    Place multiple lines of text at their respective x, y locations
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
    Run text by passing in x and y, but no text
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.text(region=region, projection=projection, x=1.2, y=2.4)


@pytest.mark.mpl_image_compare
def test_text_input_single_filename():
    """
    Run text by passing in one filename to textfiles
    """
    fig = Figure()
    fig.text(region=[10, 70, -5, 10], textfiles=POINTS_DATA)
    return fig


@pytest.mark.mpl_image_compare
def test_text_input_multiple_filenames():
    """
    Run text by passing in multiple filenames to textfiles
    """
    fig = Figure()
    fig.text(region=[10, 70, -30, 10], textfiles=[POINTS_DATA, CITIES_DATA])
    return fig


def test_text_nonexistent_filename():
    """
    Run text by passing in a list of filenames with one that does not exist
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.text(region=[10, 70, -5, 10], textfiles=[POINTS_DATA, "notexist.txt"])


@pytest.mark.mpl_image_compare
def test_text_angle_30(region, projection):
    """
    Print text at 30 degrees counter-clockwise from horizontal
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
    Print text with a bold font
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
def test_text_justify_bottom_right_and_top_left(region, projection):
    """
    Print text justified at bottom right and top left
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
    boolean operation. Loosely based on "All great-circle paths lead to Rome"
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
