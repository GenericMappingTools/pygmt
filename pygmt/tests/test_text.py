# pylint: disable=redefined-outer-name
"""
Tests text
"""
import os

import numpy as np
import pytest

from .. import Figure
from ..exceptions import GMTInvalidInput
from ..helpers import data_kind

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")


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
def test_text_input_filename(projection):
    """
    Run text by passing in a filename to textfile
    """
    fig = Figure()
    fig.text(region=[10, 70, -5, 10], projection=projection, textfile=POINTS_DATA)
    return fig


@pytest.mark.mpl_image_compare
def test_text_wrong_kind_of_input(projection):
    """
    Run text by passing in a data input that is not a file/vectors
    """
    fig = Figure()
    data = np.loadtxt(POINTS_DATA)  # Load points into numpy array
    assert data_kind(data) == "matrix"
    with pytest.raises(GMTInvalidInput):
        fig.text(region=[10, 70, -5, 10], projection=projection, textfile=data)
