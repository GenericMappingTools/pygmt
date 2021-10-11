# pylint: disable=redefined-outer-name
"""
Tests contour.
"""
import os

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from pygmt import Figure

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")


@pytest.fixture(scope="module")
def data():
    """
    Load the point data from the test file.
    """
    return pd.read_table(POINTS_DATA, header=None, sep=r"\s+")


@pytest.fixture(scope="module")
def region():
    """
    The data region.
    """
    return [10, 70, -5, 10]


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
    fig.contour(x=x, y=y, z=z, projection="X10c", region=region, frame="a", pen=True)
    return fig


@pytest.mark.mpl_image_compare(filename="test_contour_matrix.png")
@pytest.mark.parametrize(
    "array_func",
    [np.array, pd.DataFrame, xr.Dataset],
)
def test_contour_matrix(array_func, data, region):
    """
    Plot data.
    """
    fig = Figure()
    fig.contour(
        data=array_func(data), projection="X10c", region=region, frame="ag", pen=True
    )
    return fig


@pytest.mark.mpl_image_compare
def test_contour_from_file(region):
    """
    Plot using the data file name instead of loaded data.
    """
    fig = Figure()
    fig.contour(
        data=POINTS_DATA, projection="X10c", region=region, frame="af", pen="#ffcb87"
    )
    return fig


@pytest.mark.mpl_image_compare(filename="test_contour_vec.png")
def test_contour_deprecate_columns_to_incols(region):
    """
    Make sure that the old parameter "columns" is supported and it reports an
    warning.

    Modified from the test_contour_vec() test.
    """
    fig = Figure()
    x, y = np.meshgrid(
        np.linspace(region[0], region[1]), np.linspace(region[2], region[3])
    )
    x = x.flatten()
    y = y.flatten()
    z = (x - 0.5 * (region[0] + region[1])) ** 2 + 4 * y ** 2
    z = np.exp(-z / 10 ** 2 * np.log(2))

    # generate dataframe
    # switch x and y from here onwards to simulate different column order
    data = np.array([y, x, z]).T

    with pytest.warns(expected_warning=FutureWarning) as record:
        fig.contour(
            data,
            projection="X10c",
            region=region,
            frame="a",
            pen=True,
            columns=[1, 0, 2],
        )
        assert len(record) == 1  # check that only one warning was raised
    return fig
