# pylint: disable=redefined-outer-name
"""
Tests histogram.
"""
import numpy as np
import pytest
from pygmt import Figure


@pytest.fixture(scope="module")
def table():
    return [1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8]


@pytest.mark.mpl_image_compare
def test_histogram(table):
    fig = Figure()
    fig.histogram(
        table=table, projection="X10c/25c", interval=1, frame="a", fill="green"
    )
    return fig
