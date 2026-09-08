"""
Test Figure.histogram.
"""

import pandas as pd
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.params import Axis


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
        frame=Axis(annot=True),
        fill="green",
    )
    return fig


def test_histogram_baroffset(data):
    """
    Test passing bar_offset requires bar_width.
    """
    fig = Figure()
    with pytest.raises(GMTParameterError):
        fig.histogram(
            data=data,
            projection="X10c/10c",
            region=[0, 9, 0, 6],
            series=1,
            frame=Axis(annot=True),
            fill="green",
            bar_offset=0.25,
        )


@pytest.mark.mpl_image_compare(filename="test_histogram_alignment.png")
def test_histogram_alignment(data):
    """
    Test the alignment parameter.
    """
    kwargs = {
        "data": data,
        "projection": "X10c/10c",
        "region": [0, 10, 0, 8],
        "series": 1,
        "frame": Axis(annot=True),
        "pen": "1p,blue",
    }
    fig = Figure()
    fig.histogram(alignment="left", **kwargs)
    fig.shift_origin(xshift="w+1c")
    fig.histogram(alignment="center", **kwargs)
    return fig


# TODO(PyGMT>=0.22.0): Remove when the deprecated "center" parameter is removed.
@pytest.mark.mpl_image_compare(filename="test_histogram_alignment.png")
def test_histogram_deprecated_center(data):
    """
    Test the deprecated "center" parameter.
    """
    kwargs = {
        "data": data,
        "projection": "X10c/10c",
        "region": [0, 10, 0, 8],
        "series": 1,
        "frame": Axis(annot=True),
        "pen": "1p,blue",
    }
    fig = Figure()
    fig.histogram(**kwargs)
    fig.shift_origin(xshift="w+1c")
    fig.histogram(center=True, **kwargs)
    return fig


def test_histogram_align_invalid(data):
    """
    Test that an invalid align value raises an exception.
    """
    fig = Figure()
    with pytest.raises(GMTValueError):
        fig.histogram(
            data=data,
            projection="X10c/10c",
            region=[0, 9, 0, 8],
            series=1,
            alignment="bogus",
        )
