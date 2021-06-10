# pylint: disable=redefined-outer-name
"""
Tests plot.
"""
import datetime
import os

import numpy as np
import pandas as pd
import pytest
import xarray as xr
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


@pytest.mark.mpl_image_compare
def test_plot_red_circles(data, region):
    """
    Plot the data in red circles passing in vectors.
    """
    fig = Figure()
    fig.plot(
        x=data[:, 0],
        y=data[:, 1],
        region=region,
        projection="X10c",
        style="c0.2c",
        color="red",
        frame="afg",
    )
    return fig


def test_plot_fail_no_data(data):
    """
    Plot should raise an exception if no data is given.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.plot(
            region=region, projection="X10c", style="c0.2c", color="red", frame="afg"
        )
    with pytest.raises(GMTInvalidInput):
        fig.plot(
            x=data[:, 0],
            region=region,
            projection="X10c",
            style="c0.2c",
            color="red",
            frame="afg",
        )
    with pytest.raises(GMTInvalidInput):
        fig.plot(
            y=data[:, 0],
            region=region,
            projection="X10c",
            style="c0.2c",
            color="red",
            frame="afg",
        )
    # Should also fail if given too much data
    with pytest.raises(GMTInvalidInput):
        fig.plot(
            x=data[:, 0],
            y=data[:, 1],
            data=data,
            region=region,
            projection="X10c",
            style="c0.2c",
            color="red",
            frame="afg",
        )


def test_plot_fail_1d_array_with_data(data):
    """
    Should raise an exception if array color, size, intensity and transparency
    are used with matrix.
    """
    fig = Figure()
    kwargs = dict(data=data, region=region, projection="X10c", frame="afg")
    with pytest.raises(GMTInvalidInput):
        fig.plot(style="c0.2c", color=data[:, 2], **kwargs)
    with pytest.raises(GMTInvalidInput):
        fig.plot(style="cc", size=data[:, 2], color="red", **kwargs)
    with pytest.raises(GMTInvalidInput):
        fig.plot(style="c0.2c", color="red", intensity=data[:, 2], **kwargs)
    with pytest.raises(GMTInvalidInput):
        fig.plot(style="c0.2c", color="red", transparency=data[:, 2] * 100, **kwargs)


@pytest.mark.mpl_image_compare
def test_plot_projection(data):
    """
    Plot the data in green squares with a projection.
    """
    fig = Figure()
    fig.plot(
        x=data[:, 0],
        y=data[:, 1],
        region="g",
        projection="R270/10c",
        style="s0.2c",
        color="green",
        frame="ag",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_colors(data, region):
    """
    Plot the data using z as colors.
    """
    fig = Figure()
    fig.plot(
        x=data[:, 0],
        y=data[:, 1],
        color=data[:, 2],
        region=region,
        projection="X10c",
        style="c0.5c",
        cmap="cubhelix",
        frame="af",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_sizes(data, region):
    """
    Plot the data using z as sizes.
    """
    fig = Figure()
    fig.plot(
        x=data[:, 0],
        y=data[:, 1],
        size=0.5 * data[:, 2],
        region=region,
        projection="X10c",
        style="cc",
        color="blue",
        frame="af",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_colors_sizes(data, region):
    """
    Plot the data using z as sizes and colors.
    """
    fig = Figure()
    fig.plot(
        x=data[:, 0],
        y=data[:, 1],
        color=data[:, 2],
        size=0.5 * data[:, 2],
        region=region,
        projection="X10c",
        style="cc",
        cmap="copper",
        frame="af",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_colors_sizes_proj(data, region):
    """
    Plot the data using z as sizes and colors with a projection.
    """
    fig = Figure()
    fig.coast(region=region, projection="M15c", frame="af", water="skyblue")
    fig.plot(
        x=data[:, 0],
        y=data[:, 1],
        color=data[:, 2],
        size=0.5 * data[:, 2],
        style="cc",
        cmap="copper",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_varying_intensity():
    """
    Plot the data with array-like intensity.
    """
    x = np.arange(-1, 1.1, 0.1)
    y = np.zeros(x.size)
    intensity = x

    fig = Figure()
    fig.plot(
        x=x,
        y=y,
        region=[-1.1, 1.1, -0.5, 0.5],
        projection="X10c/2c",
        frame=["S", "xaf+lIntensity"],
        style="c0.25c",
        color="blue",
        intensity=intensity,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_transparency():
    """
    Plot the data with a constant transparency.
    """
    x = np.arange(1, 10)
    y = np.arange(1, 10)

    fig = Figure()
    fig.plot(
        x=x,
        y=y,
        region=[0, 10, 0, 10],
        projection="X10c",
        frame=True,
        style="c0.2c",
        color="blue",
        transparency=80.0,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_varying_transparency():
    """
    Plot the data using z as transparency.
    """
    x = np.arange(1, 10)
    y = np.arange(1, 10)
    z = np.arange(1, 10) * 10

    fig = Figure()
    fig.plot(
        x=x,
        y=y,
        region=[0, 10, 0, 10],
        projection="X10c",
        frame=True,
        style="c0.2c",
        color="blue",
        transparency=z,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_sizes_colors_transparencies():
    """
    Plot the data with varying sizes and colors using z as transparency.
    """
    x = np.arange(1.0, 10.0)
    y = np.arange(1.0, 10.0)
    color = np.arange(1, 10) * 0.15
    size = np.arange(1, 10) * 0.2
    transparency = np.arange(1, 10) * 10

    fig = Figure()
    fig.plot(
        x=x,
        y=y,
        region=[0, 10, 0, 10],
        projection="X10c",
        frame=True,
        style="cc",
        color=color,
        size=size,
        cmap="gray",
        transparency=transparency,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_matrix(data):
    """
    Plot the data passing in a matrix and specifying columns.
    """
    fig = Figure()
    fig.plot(
        data=data,
        region=[10, 70, -5, 10],
        projection="M15c",
        style="cc",
        color="#aaaaaa",
        frame="a",
        incols="0,1,2+s0.005",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_matrix_color(data):
    """
    Plot the data passing in a matrix and using a colormap.
    """
    fig = Figure()
    fig.plot(
        data=data,
        region=[10, 70, -5, 10],
        projection="X10c",
        style="c0.5c",
        cmap="rainbow",
        frame="a",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_from_file(region):
    """
    Plot using the data file name instead of loaded data.
    """
    fig = Figure()
    fig.plot(
        data=POINTS_DATA,
        region=region,
        projection="X10c",
        style="d1c",
        color="yellow",
        frame=True,
        incols=[0, 1],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_vectors():
    """
    Plot vectors.
    """
    azimuth = np.array([0, 45, 90, 135, 180, 225, 270, 310])
    lengths = np.linspace(0.1, 1, len(azimuth))
    lon = np.sin(np.deg2rad(azimuth))
    lat = np.cos(np.deg2rad(azimuth))
    fig = Figure()
    fig.plot(
        x=lon,
        y=lat,
        direction=(azimuth, lengths),
        region="-2/2/-2/2",
        projection="X10c",
        style="V0.2c+e",
        color="black",
        frame="af",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot_lines_with_arrows():
    """
    Plot lines with arrows.

    The test is slightly different from test_plot_vectors().
    Here the vectors are plotted as lines, with arrows at the end.

    The test also checks if the API crashes.
    See https://github.com/GenericMappingTools/pygmt/issues/406.
    """
    fig = Figure()
    fig.basemap(region=[-2, 2, -2, 2], frame=True)
    fig.plot(x=[-1.0, -1.0], y=[-1.0, 1.0], pen="1p,black+ve0.2c")
    fig.plot(x=[1.0, 1.0], y=[-1.0, 1.0], pen="1p,black+ve0.2c")
    return fig


@pytest.mark.mpl_image_compare
def test_plot_scalar_xy():
    """
    Plot symbols given scalar x, y coordinates.
    """
    fig = Figure()
    fig.basemap(region=[-2, 2, -2, 2], frame=True)
    fig.plot(x=-1.5, y=1.5, style="c1c")
    fig.plot(x=0, y=0, style="t1c")
    fig.plot(x=1.5, y=-1.5, style="s1c")
    return fig


@pytest.mark.mpl_image_compare
def test_plot_datetime():
    """
    Test various datetime input data.
    """
    fig = Figure()
    fig.basemap(
        projection="X15c/5c",
        region=[
            np.array("2010-01-01T00:00:00", dtype=np.datetime64),
            pd.Timestamp("2020-01-01"),
            0,
            10,
        ],
        frame=True,
    )

    # numpy.datetime64 types
    x = np.array(
        ["2010-06-01", "2011-06-01T12", "2012-01-01T12:34:56"], dtype="datetime64"
    )
    y = [1.0, 2.0, 3.0]
    fig.plot(x, y, style="c0.2c", pen="1p")

    # pandas.DatetimeIndex
    x = pd.date_range("2013", freq="YS", periods=3)
    y = [4, 5, 6]
    fig.plot(x, y, style="t0.2c", pen="1p")

    # xarray.DataArray
    x = xr.DataArray(data=pd.date_range(start="2015-03", freq="QS", periods=3))
    y = [7.5, 6, 4.5]
    fig.plot(x, y, style="s0.2c", pen="1p")

    # raw datetime strings
    x = ["2016-02-01", "2017-03-04T00:00"]
    y = [7, 8]
    fig.plot(x, y, style="a0.2c", pen="1p")

    # the Python built-in datetime and date
    x = [datetime.date(2018, 1, 1), datetime.datetime(2019, 1, 1)]
    y = [8.5, 9.5]
    fig.plot(x, y, style="i0.2c", pen="1p")
    return fig


@pytest.mark.mpl_image_compare(filename="test_plot_sizes.png")
def test_plot_deprecate_sizes_to_size(data, region):
    """
    Make sure that the old parameter "sizes" is supported and it reports a
    warning.

    Modified from the test_plot_sizes() test.
    """
    fig = Figure()
    with pytest.warns(expected_warning=FutureWarning) as record:
        fig.plot(
            x=data[:, 0],
            y=data[:, 1],
            sizes=0.5 * data[:, 2],
            region=region,
            projection="X10c",
            style="cc",
            color="blue",
            frame="af",
        )
        assert len(record) == 1  # check that only one warning was raised
    return fig


@pytest.mark.mpl_image_compare(filename="test_plot_from_file.png")
def test_plot_deprecate_columns_to_incols(region):
    """
    Make sure that the old parameter "columns" is supported and it reports a
    warning.

    Modified from the test_plot_from_file() test.
    """
    fig = Figure()
    with pytest.warns(expected_warning=FutureWarning) as record:
        fig.plot(
            data=POINTS_DATA,
            region=region,
            projection="X10c",
            style="d1c",
            color="yellow",
            frame=True,
            columns=[0, 1],
        )
        assert len(record) == 1  # check that only one warning was raised
    return fig
