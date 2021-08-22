"""
Tests plot3d.
"""
import os
import sys

import numpy as np
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the point data from the test file.
    """
    return np.loadtxt(POINTS_DATA)


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    The data region.
    """
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
        projection="X10c",
        style="c0.2c",
        color="red",
        frame=["afg", "zafg"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_red_circles_zsize(data, region):
    "Plot the 3D data in red circles passing in vectors and setting zsize = 6c"
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zsize="6c",
        perspective=[225, 30],
        region=region,
        projection="X10c",
        style="c0.2c",
        color="red",
        frame=["afg", "zafg"],
    )
    return fig


def test_plot3d_fail_no_data(data, region):
    """
    Plot should raise an exception if no data is given.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(
            region=region, projection="X10c", style="c0.2c", color="red", frame="afg"
        )
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(
            x=data[:, 0],
            region=region,
            projection="X10c",
            style="c0.2c",
            color="red",
            frame="afg",
        )
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(
            y=data[:, 0],
            region=region,
            projection="X10c",
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
            projection="X10c",
            style="c0.2c",
            color="red",
            frame="afg",
        )


def test_plot3d_fail_1d_array_with_data(data, region):
    """
    Should raise an exception if array color, size, intensity and transparency
    are used with matrix.
    """
    fig = Figure()
    kwargs = dict(data=data, region=region, projection="X10c", frame="afg")
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(style="c0.2c", color=data[:, 2], **kwargs)
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(style="cc", size=data[:, 2], color="red", **kwargs)
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(style="cc", intensity=data[:, 2], color="red", **kwargs)
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(style="cc", color="red", transparency=data[:, 2] * 100, **kwargs)


@pytest.mark.mpl_image_compare
def test_plot3d_projection(data, region):
    """
    Plot the data in green squares with a projection.
    """
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="R270/10c",
        style="s1c",
        color="green",
        frame=["ag", "zag"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_colors(data, region):
    """
    Plot the data using z as colors.
    """
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        color=data[:, 2],
        region=region,
        projection="X6c",
        style="c0.5c",
        cmap="cubhelix",
        frame=["afg", "zafg"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_sizes(data, region):
    """
    Plot the data using z as sizes.
    """
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        size=0.5 * data[:, 2],
        region=region,
        projection="X10c",
        # Using inches instead of cm because of upstream bug at
        # https://github.com/GenericMappingTools/gmt/issues/4386
        style="ui",
        color="blue",
        frame=["af", "zaf"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_colors_sizes(data, region):
    """
    Plot the data using z as sizes and colors.
    """
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        color=data[:, 2],
        size=0.5 * data[:, 2],
        region=region,
        projection="X6c",
        # Using inches instead of cm because of upstream bug at
        # https://github.com/GenericMappingTools/gmt/issues/4386
        style="ui",
        cmap="copper",
        frame=["af", "zaf"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_colors_sizes_proj(data, region):
    """
    Plot the data using z as sizes and colors with a projection.
    """
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="M20c",
        frame=["af", "zaf"],
        color=data[:, 2],
        size=data[:, 2],
        # Using inches instead of cm because of upstream bug at
        # https://github.com/GenericMappingTools/gmt/issues/4386
        style="ui",
        cmap="copper",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_varying_intensity():
    """
    Plot the data with array-like intensity.
    """
    x = np.arange(-1, 1.1, 0.1)
    y = np.zeros(x.size)
    z = y
    intensity = x

    fig = Figure()
    fig.plot3d(
        x=x,
        y=y,
        z=z,
        region=[-1.1, 1.1, -0.5, 0.5, -0.5, 0.5],
        projection="X15c/5c",
        zsize="5c",
        perspective=[135, 30],
        frame=["Sltr", "xaf+lIntensity"],
        style="c0.5c",
        color="blue",
        intensity=intensity,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_transparency():
    """
    Plot the data with a constant transparency.
    """
    x = np.arange(1, 10)
    y = np.arange(1, 10)
    z = np.arange(1, 10) * 10

    fig = Figure()
    fig.plot3d(
        x=x,
        y=y,
        z=z,
        style="u0.2c",
        color="blue",
        region=[0, 10, 0, 10, 10, 90],
        projection="X10c",
        zscale=0.1,
        frame=True,
        perspective=[135, 30],
        transparency=80.0,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_varying_transparency():
    """
    Plot the data using z as transparency using 3-D column symbols.
    """
    x = np.arange(1, 10)
    y = np.arange(1, 10)
    z = np.arange(1, 10) * 10

    fig = Figure()
    fig.plot3d(
        x=x,
        y=y,
        z=z,
        style="o0.2c+B5",
        color="blue",
        region=[0, 10, 0, 10, 10, 90],
        projection="X10c",
        zscale=0.1,
        frame=True,
        perspective=[135, 30],
        transparency=z,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_sizes_colors_transparencies():
    """
    Plot the data with varying sizes and colors using z as transparency.
    """
    x = np.arange(1.0, 10.0)
    y = np.arange(1.0, 10.0)
    z = np.arange(1, 10) * 10
    color = np.arange(1, 10) * 0.15
    size = np.arange(1, 10) * 0.2
    transparency = np.arange(1, 10) * 10

    fig = Figure()
    fig.plot3d(
        x=x,
        y=y,
        z=z,
        region=[0, 10, 0, 10, 10, 90],
        projection="X10c",
        zscale=0.1,
        perspective=[135, 30],
        frame=True,
        style="uc",
        color=color,
        size=size,
        cmap="gray",
        transparency=transparency,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_matrix(data, region):
    """
    Plot the data passing in a matrix and specifying incols.
    """
    fig = Figure()
    fig.plot3d(
        data=data,
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="M20c",
        style="c1c",
        color="#aaaaaa",
        frame=["a", "za"],
        incols="0,1,2",
    )
    return fig


@pytest.mark.xfail(
    condition=sys.platform == "win32",
    reason="Wrong plot generated on Windows due to incorrect -i parameter parsing",
)
@pytest.mark.mpl_image_compare
def test_plot3d_matrix_color(data, region):
    """
    Plot the data passing in a matrix and using a colormap.
    """
    fig = Figure()
    fig.plot3d(
        data=data,
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="X10c",
        style="c0.5c",
        cmap="rainbow",
        incols=[0, 1, 2, 2],
        frame=["a", "za"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_from_file(region):
    """
    Plot using the data file name instead of loaded data.
    """
    fig = Figure()
    fig.plot3d(
        data=POINTS_DATA,
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="X20c",
        style="d1c",
        color="yellow",
        frame=["af", "zaf"],
        incols=[0, 1, 2],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_vectors():
    """
    Plot vectors.
    """
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
        region=[-2, 2, -2, 2, -2, 2],
        projection="X10c",
        style="V1c+e",
        color="black",
        frame=["af", "zaf"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_scalar_xyz():
    """
    Plot symbols given scalar x, y, z coordinates.
    """
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


@pytest.mark.mpl_image_compare(filename="test_plot3d_sizes.png")
def test_plot3d_deprecate_sizes_to_size(data, region):
    """
    Make sure that the old parameter "sizes" is supported and it reports an
    warning.

    Modified from the test_plot3d_sizes() test.
    """
    fig = Figure()
    with pytest.warns(expected_warning=FutureWarning) as record:
        fig.plot3d(
            x=data[:, 0],
            y=data[:, 1],
            z=data[:, 2],
            zscale=5,
            perspective=[225, 30],
            sizes=0.5 * data[:, 2],
            region=region,
            projection="X10c",
            style="ui",
            color="blue",
            frame=["af", "zaf"],
        )
        assert len(record) == 1  # check that only one warning was raised
    return fig


@pytest.mark.mpl_image_compare(filename="test_plot3d_matrix.png")
def test_plot3d_deprecate_columns_to_incols(data, region):
    """
    Make sure that the old parameter "columns" is supported and it reports an
    warning.

    Modified from the test_plot3d_matrix() test.
    """
    fig = Figure()
    with pytest.warns(expected_warning=FutureWarning) as record:
        fig.plot3d(
            data=data,
            zscale=5,
            perspective=[225, 30],
            region=region,
            projection="M20c",
            style="c1c",
            color="#aaaaaa",
            frame=["a", "za"],
            columns="0,1,2",
        )
        assert len(record) == 1  # check that only one warning was raised
    return fig
