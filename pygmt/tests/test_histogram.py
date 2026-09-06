"""
Test Figure.histogram.
"""

import numpy as np
import pandas as pd
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTParameterError, GMTTypeError
from pygmt.helpers import GMTTempFile
from pygmt.params import Axis


@pytest.fixture(scope="module", name="data", params=[list, pd.Series])
def fixture_data(request):
    """
    Return a list of integers to be used in the histogram.
    """
    data = [1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8]
    return request.param(data)


@pytest.fixture(scope="module", name="weights")
def fixture_weights():
    """
    Return a list of weights to be used in the histogram.
    """
    return [
        0.1,
        0.1,
        0.2,
        0.2,
        0.3,
        0.3,
        0.4,
        0.4,
        0.5,
        0.5,
        0.6,
        0.6,
        0.7,
        0.7,
        0.8,
        0.8,
        0.9,
        0.9,
        1.0,
        1.0,
    ]


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
            region=[0, 10, 0, 6],
            series=1,
            frame=Axis(annot=True),
            fill="green",
            bar_offset=0.25,
        )


@pytest.mark.mpl_image_compare(filename="test_histogram_weights.png")
def test_histogram_weights_file(data, weights):
    """
    Test weights given in the second column of a data file.
    """
    kwargs = {
        "series": 1,
        "region": [0, 10, 0, 6],
        "projection": "X8c/5c",
        "frame": Axis(annot=True),
        "fill": "lightblue",
    }
    with GMTTempFile() as tmpfile:
        np.savetxt(
            tmpfile.name, np.column_stack([data, weights]), header="data,weights"
        )
        fig = Figure()
        fig.histogram(data=tmpfile.name, weights=True, **kwargs)
        return fig


@pytest.mark.mpl_image_compare(filename="test_histogram_weights.png")
def test_histogram_weights_2darray(data, weights):
    """
    Test weights given in the second column of a 2-D sequence.
    """
    kwargs = {
        "series": 1,
        "region": [0, 10, 0, 6],
        "projection": "X8c/5c",
        "frame": Axis(annot=True),
        "fill": "lightblue",
    }
    _data = np.column_stack([data, weights])
    fig = Figure()
    fig.histogram(data=_data, weights=True, **kwargs)
    return fig


@pytest.mark.mpl_image_compare(filename="test_histogram_weights.png")
def test_histogram_weights_array(data, weights):
    """
    Test weights given as a 1-D array alongside 1-D data.
    """
    kwargs = {
        "series": 1,
        "region": [0, 10, 0, 6],
        "projection": "X8c/5c",
        "frame": Axis(annot=True),
        "fill": "lightblue",
    }
    fig = Figure()
    fig.histogram(data=data, weights=weights, **kwargs)
    return fig


def test_histogram_weights_array_invalid_data():
    """
    Test that passing weights as an array requires data to be a 1-D sequence.
    """
    fig = Figure()
    with pytest.raises(GMTTypeError):
        fig.histogram(data="input.txt", series=1, weights=[0.5, 1.0, 2.0])
