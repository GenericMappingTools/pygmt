"""
Test Figure.histogram.
"""

import pandas as pd
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


@pytest.fixture(scope="module", name="data", params=[list, pd.Series])
def fixture_data(request):
    """
    Return a list of integers to be used in the histogram.
    """
    data = [1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8]
    return request.param(data)


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare(filename="test_histogram.png")
def test_histogram(data):
    """
    Test plotting a histogram using a sequence of integers from a table.
    """
    fig = Figure()
    fig.histogram(
        data=data,
        projection="X10c/10c",
        region=[0, 9, 0, 6],
        series=1,
        frame="a",
        fill="green",
    )
    return fig


def test_histogram_barwidth_baroffset(data):
    """
    Test plotting a histogram specifying bar_with and bar_offset.
    """
    fig = Figure()
    fig.histogram(
        data=data,
        projection="X10c/10c",
        region=[0, 9, 0, 6],
        series=1,
        frame="a",
        fill="green",
        bar_width=0.5,
        bar_offset=0.25,
    )
    return fig


def test_histogram_baroffset(data):
    """
    Test passing bar_offset requires bar_width.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.histogram(
            data=data,
            projection="X10c/10c",
            region=[0, 9, 0, 6],
            series=1,
            frame="a",
            fill="green",
            bar_offset=0.25,
        )
