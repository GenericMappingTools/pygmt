"""
Test Figure.contour.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from pygmt import Figure

POINTS_DATA = Path(__file__).parent / "data" / "points.txt"


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the point data from the test file.
    """
    return pd.read_table(POINTS_DATA, header=None, sep=r"\s+")


@pytest.fixture(scope="module", name="region")
def fixture_region():
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
    z = (x - 0.5 * (region[0] + region[1])) ** 2 + 4 * y**2
    z = np.exp(-z / 10**2 * np.log(2))
    fig.contour(x=x, y=y, z=z, projection="X10c", region=region, frame="a", pen=True)
    return fig


@pytest.mark.benchmark
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


@pytest.mark.mpl_image_compare
def test_contour_interval(region):
    """
    Plot data with fixed (different) contour and annotation intervals.
    """
    fig = Figure()
    fig.contour(
        data=POINTS_DATA,
        projection="X10c",
        region=region,
        frame="af",
        levels=0.1,
        annotation=0.2,
        pen=True,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_contour_one_level(region):
    """
    Plot data with one contour level and one (different) annotation level.
    """
    fig = Figure()
    fig.contour(
        data=POINTS_DATA,
        projection="X10c",
        region=region,
        frame="af",
        levels=[0.4],
        annotation=[0.5],
        pen=True,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_contour_multiple_levels(region):
    """
    Plot data with multiple (different) contour and annotation levels.
    """
    fig = Figure()
    fig.contour(
        data=POINTS_DATA,
        projection="X10c",
        region=region,
        frame="af",
        levels=[0.2, 0.3],
        annotation=[0.4, 0.45],
        pen=True,
    )
    return fig


@pytest.mark.mpl_image_compare(filename="test_contour_vec.png")
def test_contour_incols_transposed_data(region):
    """
    Make sure that transposing the data matrix still produces a correct result with
    incols reordering the columns.

    This is a regression test for
    https://github.com/GenericMappingTools/pygmt/issues/1313

    Modified from the test_contour_vec() test.
    """
    fig = Figure()
    x, y = np.meshgrid(
        np.linspace(region[0], region[1]), np.linspace(region[2], region[3])
    )
    x = x.flatten()
    y = y.flatten()
    z = (x - 0.5 * (region[0] + region[1])) ** 2 + 4 * y**2
    z = np.exp(-z / 10**2 * np.log(2))

    # generate dataframe
    # switch x and y from here onwards to simulate different column order
    data = np.array([y, x, z]).T

    fig.contour(
        data,
        projection="X10c",
        region=region,
        frame="a",
        pen=True,
        incols=[1, 0, 2],
    )
    return fig
