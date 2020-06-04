# pylint: disable=redefined-outer-name
"""
Tests plot3d.
"""
import os

import numpy as np
import pytest

from .. import Figure
from ..exceptions import GMTInvalidInput


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")


@pytest.fixture(scope="module")
def data():
    "Load the point data from the test file"
    return np.loadtxt(POINTS_DATA)


@pytest.fixture(scope="module")
def region():
    "The data region"
    return [10, 70, -5, 10, 0, 1]


@pytest.mark.mpl_image_compare
def test_plot3d_red_circles_zscale(data, region):
    "Plot the 3D data in red circles passing in vectors and setting zscale = 5"
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="X4i",
        style="c0.2c",
        color="red",
        frame=["afg", "zafg"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_red_circles_zsize(data, region):
    "Plot the 3D data in red circles passing in vectors and setting zsize = 3i"
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zsize="3i",
        perspective=[225, 30],
        region=region,
        projection="X4i",
        style="c0.2c",
        color="red",
        frame=["afg", "zafg"],
    )
    return fig


def test_plot3d_fail_no_data(data):
    "Plot should raise an exception if no data is given"
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(
            region=region, projection="X4i", style="c0.2c", color="red", frame="afg"
        )
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(
            x=data[:, 0],
            region=region,
            projection="X4i",
            style="c0.2c",
            color="red",
            frame="afg",
        )
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(
            y=data[:, 0],
            region=region,
            projection="X4i",
            style="c0.2c",
            color="red",
            frame="afg",
        )
    # Should also fail if given too much data
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(
            x=data[:, 0],
            y=data[:, 1],
            z=data[:, 2],
            data=data,
            region=region,
            projection="X4i",
            style="c0.2c",
            color="red",
            frame="afg",
        )


def test_plot3d_fail_size_color(data):
    "Should raise an exception if array sizes and color are used with matrix"
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(
            data=data,
            region=region,
            projection="X4i",
            style="c0.2c",
            color=data[:, 2],
            frame="afg",
        )
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(
            data=data,
            region=region,
            projection="X4i",
            style="cc",
            sizes=data[:, 2],
            color="red",
            frame="afg",
        )


@pytest.mark.mpl_image_compare
def test_plot3d_projection(data, region):
    "Plot the data in green squares with a projection"
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="R270/4i",
        style="s1c",
        color="green",
        frame=["ag", "zag"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_colors(data, region):
    "Plot the data using z as colors"
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        color=data[:, 2],
        region=region,
        projection="X3i",
        style="c0.5c",
        cmap="cubhelix",
        frame=["afg", "zafg"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_sizes(data, region):
    "Plot the data using z as sizes"
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        sizes=0.5 * data[:, 2],
        region=region,
        projection="X4i",
        style="cc",
        color="blue",
        frame=["af", "zaf"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_colors_sizes(data, region):
    "Plot the data using z as sizes and colors"
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        color=data[:, 2],
        sizes=0.5 * data[:, 2],
        region=region,
        projection="X3i",
        style="cc",
        cmap="copper",
        frame=["af", "zaf"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_colors_sizes_proj(data, region):
    "Plot the data using z as sizes and colors with a projection"
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="M10i",
        frame=["af", "zaf"],
        color=data[:, 2],
        sizes=data[:, 2],
        style="cc",
        cmap="copper",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_matrix(data, region):
    "Plot the data passing in a matrix and specifying columns"
    fig = Figure()
    fig.plot3d(
        data=data,
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="M10i",
        style="c1c",
        color="#aaaaaa",
        frame=["a", "za"],
        columns="0,1,2",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_matrix_color(data, region):
    "Plot the data passing in a matrix and using a colormap"
    fig = Figure()
    fig.plot3d(
        data=data,
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="X5i",
        style="c0.5c",
        cmap="rainbow",
        columns=[0, 1, 2, 2],
        frame=["a", "za"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_from_file(region):
    "Plot using the data file name instead of loaded data"
    fig = Figure()
    fig.plot3d(
        data=POINTS_DATA,
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="X10i",
        style="d1c",
        color="yellow",
        frame=["af", "zaf"],
        columns=[0, 1, 2],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_vectors():
    "Plot vectors"
    azimuth = np.array([0, 45, 90, 135, 180, 225, 270, 310])
    lengths = np.linspace(0.1, 1, len(azimuth))
    lon = np.sin(np.deg2rad(azimuth))
    lat = np.cos(np.deg2rad(azimuth))
    elev = np.tan(np.deg2rad(azimuth))
    fig = Figure()
    fig.plot3d(
        x=lon,
        y=lat,
        z=elev,
        zscale=2,
        perspective=[225, 30],
        direction=(azimuth, lengths),
        region="-2/2/-2/2/-2/2",
        projection="X4i",
        style="V1c+e",
        color="black",
        frame=["af", "zaf"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_scalar_xyz():
    "Plot symbols given scalar x, y, z coordinates"
    fig = Figure()
    fig.basemap(
        region=[-2, 2, -2, 2, -2, 2],
        frame=["xaf+lx", "yaf+ly", "zaf+lz"],
        zscale=2,
        perspective=[225, 30],
    )
    fig.plot3d(
        x=-1.5, y=1.5, z=-1.5, style="c1c", color="red", zscale=True, perspective=True
    )
    fig.plot3d(x=0, y=0, z=0, style="t1c", color="green", zscale=True, perspective=True)
    fig.plot3d(
        x=1.5, y=-1.5, z=1.5, style="s1c", color="blue", zscale=True, perspective=True
    )
    return fig
