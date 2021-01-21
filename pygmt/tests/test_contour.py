# pylint: disable=redefined-outer-name
"""
Tests contour.
"""
import os
from itertools import product

import numpy as np
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")


@pytest.fixture(scope="module")
def data():
    """
    Load the point data from the test file.
    """
    return np.loadtxt(POINTS_DATA)


@pytest.fixture(scope="module")
def region():
    """
    The data region.
    """
    return [10, 70, -5, 10]


def test_contour_fail_no_data(data):
    """
    Should raise an exception if no data is given.
    """
    # Contour should raise an exception if no or not sufficient data
    # is given
    fig = Figure()
    # Test all combinations where at least one data variable
    # is not given:
    for variable in product([None, data[:, 0]], repeat=3):
        # Filter one valid configuration:
        if not any(item is None for item in variable):
            continue
        with pytest.raises(GMTInvalidInput):
            fig.contour(
                x=variable[0],
                y=variable[1],
                z=variable[2],
                region=region,
                projection="X4i",
                color="red",
                frame="afg",
                pen="",
            )
    # Should also fail if given too much data
    with pytest.raises(GMTInvalidInput):
        fig.contour(
            x=data[:, 0],
            y=data[:, 1],
            z=data[:, 2],
            data=data,
            region=region,
            projection="X4i",
            style="c0.2c",
            color="red",
            frame="afg",
            pen="",
        )


@pytest.mark.mpl_image_compare
def test_contour_vec(region):
    """
    Plot an x-centered gaussian kernel with different y scale.
    """
    fig = Figure()
    x, y = np.meshgrid(
        np.linspace(region[0], region[1]), np.linspace(region[2], region[3])
    )
    x = x.flatten()
    y = y.flatten()
    z = (x - 0.5 * (region[0] + region[1])) ** 2 + 4 * y ** 2
    z = np.exp(-z / 10 ** 2 * np.log(2))
    fig.contour(x=x, y=y, z=z, projection="X4i", region=region, frame="a", pen="")
    return fig


@pytest.mark.mpl_image_compare
def test_contour_matrix(data, region):
    """
    Plot data.
    """
    fig = Figure()
    fig.contour(data=data, projection="X3i", region=region, frame="ag", pen="")
    return fig


@pytest.mark.mpl_image_compare
def test_contour_from_file(region):
    """
    Plot using the data file name instead of loaded data.
    """
    fig = Figure()
    fig.contour(
        data=POINTS_DATA, projection="X4i", region=region, frame="af", pen="#ffcb87"
    )
    return fig
