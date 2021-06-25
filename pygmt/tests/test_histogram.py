# pylint: disable=redefined-outer-name
"""
Tests histogram.
"""
import pandas as pd
import pytest
from pygmt import Figure


@pytest.fixture(scope="module", name="table", params=[list, pd.Series])
def fixture_table(request):
    """
    Returns a list of integers to be used in the histogram.
    """
    data = [1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8]
    return request.param(data)


@pytest.mark.mpl_image_compare(filename="test_histogram.png")
def test_histogram(table):
    """
    Tests plotting a histogram using a sequence of integers from a table.
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
