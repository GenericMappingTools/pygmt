"""
Tests wiggle.
"""
import numpy as np
import pytest
from pygmt import Figure


@pytest.mark.mpl_image_compare
def test_wiggle():
    """
    Plot the z=f(x,y) anomalies along tracks.
    """
    x = np.arange(-2, 2, 0.02)
    y = np.zeros(x.size)
    z = np.cos(2 * np.pi * x)

    fig = Figure()
    fig.wiggle(
        region=[-4, 4, -1, 1],
        projection="X8c",
        x=x,
        y=y,
        z=z,
        scale="0.5c",
        color=["red+p", "gray+n"],
        pen="1.0p",
        track="0.5p",
        position="jRM+w2+lnT",
    )
    return fig


@pytest.mark.mpl_image_compare(filename="test_wiggle.png")
def test_wiggle_data_incols():
    """
    Make sure that incols parameter works with input data array.
    """

    # put data into numpy array and swap x and y columns
    # as the use of the 'incols' parameter will reverse this action
    x = np.arange(-2, 2, 0.02)
    y = np.zeros(x.size)
    z = np.cos(2 * np.pi * x)
    data = np.array([y, x, z]).T

    fig = Figure()
    fig.wiggle(
        data,
        region=[-4, 4, -1, 1],
        projection="X8c",
        incols=[1, 0, 2],
        scale="0.5c",
        color=["red+p", "gray+n"],
        pen="1.0p",
        track="0.5p",
        position="jRM+w2+lnT",
    )
    return fig
