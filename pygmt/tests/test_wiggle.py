"""
Test Figure.wiggle.
"""

import numpy as np
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTParameterError
from pygmt.params import Position


@pytest.fixture(scope="module", name="data")
def fixture_xyz():
    """
    Create sample (x, y, z) data for testing.
    """
    x = np.arange(-2, 2, 0.02)
    y = np.zeros(x.size)
    z = np.cos(2 * np.pi * x)
    return (x, y, z)


@pytest.mark.mpl_image_compare
def test_wiggle(data):
    """
    Plot the z=f(x,y) anomalies along tracks.
    """
    x, y, z = data
    fig = Figure()
    fig.wiggle(
        region=[-4, 4, -1, 1],
        projection="X8c",
        x=x,
        y=y,
        z=z,
        scale="0.5c",
        positive_fill="red",
        negative_fill="gray",
        pen="1.0p",
        track="0.5p",
        position=Position("MR"),
        length=2,
        label="nT",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_wiggle_default_position(data):
    """
    Test that wiggle works when position is not provided.
    """
    x, y, z = data
    fig = Figure()
    fig.wiggle(
        region=[-4, 4, -1, 1],
        projection="X8c",
        frame=True,
        x=x,
        y=y,
        z=z,
        pen="1p",
        scale="0.5c",
        length=1,
    )
    return fig


@pytest.mark.mpl_image_compare(filename="test_wiggle.png")
def test_wiggle_deprecated_position_syntax(data):
    """
    Test the deprecated position syntax for wiggle.
    """
    x, y, z = data
    fig = Figure()
    fig.wiggle(
        region=[-4, 4, -1, 1],
        projection="X8c",
        x=x,
        y=y,
        z=z,
        scale="0.5c",
        positive_fill="red",
        negative_fill="gray",
        pen="1.0p",
        track="0.5p",
        position="jMR+w2+lnT",
    )
    return fig


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare(filename="test_wiggle.png")
def test_wiggle_data_incols(data):
    """
    Make sure that incols parameter works with input data array.
    """
    # put data into numpy array and swap x and y columns
    # as the use of the 'incols' parameter will reverse this action
    x, y, z = data
    data = np.array([y, x, z]).T

    fig = Figure()
    fig.wiggle(
        data,
        region=[-4, 4, -1, 1],
        projection="X8c",
        incols=[1, 0, 2],
        scale="0.5c",
        positive_fill="red",
        negative_fill="gray",
        pen="1.0p",
        track="0.5p",
        position=Position("MR"),
        length=2,
        label="nT",
    )
    return fig


def test_wiggle_mixed_syntax(data):
    """
    Test that an error is raised when mixing new and deprecated syntax in 'position'.
    """
    x, y, z = data
    fig = Figure()
    kwargs = {
        "region": [-4, 4, -1, 1],
        "projection": "X8c",
        "x": x,
        "y": y,
        "z": z,
        "scale": "0.5c",
        "positive_fill": "red",
        "negative_fill": "gray",
        "pen": "1.0p",
        "track": "0.5p",
    }
    with pytest.raises(GMTParameterError):
        fig.wiggle(position="jMR+w2+lnT", length=2, **kwargs)

    with pytest.raises(GMTParameterError):
        fig.wiggle(position="jMR+w2+lnT", label="nT", **kwargs)

    with pytest.raises(GMTParameterError):
        fig.wiggle(position="jMR+w2+lnT", label_alignment="left", **kwargs)
