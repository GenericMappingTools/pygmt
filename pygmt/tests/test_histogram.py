# pylint: disable=redefined-outer-name
"""
Tests histogram.
"""
import pytest
from pygmt import Figure


@pytest.fixture(scope="module")
def table():
    """
    Returns a list of integers to be used in the histogram.
    """
    return [1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8]


@pytest.mark.mpl_image_compare
def test_histogram(table):
    """
    Tests plotting a histogram using a list of integers.
    """
    fig = Figure()
    fig.histogram(
        table=table,
        projection="X10c/10c",
        region=[0, 9, 0, 6],
        series=1,
        frame="a",
        fill="green",
    )
    return fig
