"""
Test Figure.histogram.
"""

import pandas as pd
import pytest
from pygmt import Figure, makecpt
from pygmt.exceptions import GMTParameterError
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


@pytest.mark.mpl_image_compare(filename="test_histogram_fill.png")
def test_histogram_fill(data):
    """
    Test filling bars with constant color and lookup table values.
    """
    kwargs = {
        "data": data,
        "projection": "X5c/5c",
        "region": [0, 10, 0, 8],
        "series": 1,
        "frame": Axis(annot=True),
    }
    fig = Figure()
    # Constant fill
    fig.histogram(fill="green", **kwargs)
    fig.shift_origin(xshift=6)
    # Fill bars by bin position
    makecpt(cmap="viridis", series=[0, 9, 1])
    fig.histogram(fill="position", **kwargs)
    fig.colorbar(frame=True)
    # Fill bars by bin value
    fig.shift_origin(xshift=6)
    makecpt(cmap="viridis", series=[0, 6, 1])
    fig.histogram(fill="value", **kwargs)
    fig.colorbar(frame=True)
    return fig

@pytest.mark.mpl_image_compare(filename="test_histogram_fill.png")
def test_histogram_fill_old_cmap_syntax(data):
    """
    Test filling bars with constant color and lookup table values.
    """
    kwargs = {
        "data": data,
        "projection": "X5c/5c",
        "region": [0, 10, 0, 8],
        "series": 1,
        "frame": Axis(annot=True),
    }
    fig = Figure()
    # Constant fill
    fig.histogram(fill="green", **kwargs)
    fig.shift_origin(xshift=6)
    # Fill bars by bin position
    makecpt(cmap="viridis", series=[0, 9, 1])
    fig.histogram(cmap=True, **kwargs)
    fig.colorbar(frame=True)
    # Fill bars by bin value
    fig.shift_origin(xshift=6)
    makecpt(cmap="viridis", series=[0, 6, 1])
    fig.histogram(cmap="+b", **kwargs)
    fig.colorbar(frame=True)
    return fig


def test_histogram_fill_color_with_cmap(data):
    """
    Test that a constant fill color cannot be combined with cmap.
    """
    fig = Figure()
    with pytest.raises(GMTParameterError):
        fig.histogram(
            data=data,
            projection="X10c/10c",
            region=[0, 9, 0, 8],
            series=1,
            cmap=True,
            fill="green",
        )
