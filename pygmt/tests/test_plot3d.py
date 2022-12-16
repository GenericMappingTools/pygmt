"""
Tests plot3d.
"""
import os
from pathlib import Path

import numpy as np
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile

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
    """
    Plot the 3-D data in red circles passing in vectors and setting
    zscale = 5
    """
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
        fill="red",
        frame=["afg", "zafg"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_red_circles_zsize(data, region):
    """
    Plot the 3-D data in red circles passing in vectors and setting
    zsize = "6c"
    """
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
        fill="red",
        frame=["afg", "zafg"],
    )
    return fig


def test_plot3d_fail_1d_array_with_data(data, region):
    """
    Should raise an exception if array fill, size, intensity and transparency
    are used with matrix.
    """
    fig = Figure()
    kwargs = dict(data=data, region=region, projection="X10c", frame="afg")
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(style="c0.2c", fill=data[:, 2], **kwargs)
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(style="cc", size=data[:, 2], fill="red", **kwargs)
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(style="cc", intensity=data[:, 2], fill="red", **kwargs)
    with pytest.raises(GMTInvalidInput):
        fig.plot3d(style="cc", fill="red", transparency=data[:, 2] * 100, **kwargs)


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
        fill="green",
        frame=["ag", "zag"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_colors(data, region):
    """
    Plot the data using z as fills.
    """
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        fill=data[:, 2],
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
        fill="blue",
        frame=["af", "zaf"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_colors_sizes(data, region):
    """
    Plot the data using z as sizes and fills.
    """
    fig = Figure()
    fig.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        fill=data[:, 2],
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
    Plot the data using z as sizes and fills with a projection.
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
        fill=data[:, 2],
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
        fill="blue",
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
        fill="blue",
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
        fill="blue",
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
    Plot the data with varying sizes and fills using z as transparency.
    """
    x = np.arange(1.0, 10.0)
    y = np.arange(1.0, 10.0)
    z = np.arange(1, 10) * 10
    fill = np.arange(1, 10) * 0.15
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
        fill=fill,
        size=size,
        cmap="gray",
        transparency=transparency,
    )
    return fig


@pytest.mark.mpl_image_compare
@pytest.mark.mpl_image_compare(filename="test_plot3d_matrix.png")
@pytest.mark.parametrize("fill", ["#aaaaaa", 170])
def test_plot3d_matrix(data, region, fill):
    """
    Plot the data passing in a matrix and specifying incols.
    """
    fig = Figure()
    fig.plot3d(
        data,
        zscale=5,
        perspective=[225, 30],
        region=region,
        projection="M20c",
        style="c1c",
        fill=fill,
        frame=["a", "za"],
        incols="0,1,2",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_plot3d_matrix_color(data, region):
    """
    Plot the data passing in a matrix and using a colormap.
    """
    fig = Figure()
    fig.plot3d(
        data,
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
        fill="yellow",
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
        style="V1c+e+n",
        fill="black",
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
        x=-1.5, y=1.5, z=-1.5, style="c1c", fill="red", zscale=True, perspective=True
    )
    fig.plot3d(x=0, y=0, z=0, style="t1c", fill="green", zscale=True, perspective=True)
    fig.plot3d(
        x=1.5, y=-1.5, z=1.5, style="s1c", fill="blue", zscale=True, perspective=True
    )
    return fig


@pytest.mark.mpl_image_compare(
    filename="test_plot3d_ogrgmt_file_multipoint_default_style.png"
)
@pytest.mark.parametrize("func", [str, Path])
def test_plot3d_ogrgmt_file_multipoint_default_style(func):
    """
    Make sure that OGR/GMT files with MultiPoint geometry are plotted as cubes
    and not as line (default GMT style).
    """
    with GMTTempFile(suffix=".gmt") as tmpfile:
        gmt_file = """# @VGMT1.0 @GMULTIPOINT
# @R1/1.5/1/1.5
# FEATURE_DATA
>
1 1 2
1.5 1.5 1"""
        with open(tmpfile.name, "w", encoding="utf8") as file:
            file.write(gmt_file)
        fig = Figure()
        fig.plot3d(
            data=func(tmpfile.name),
            perspective=[315, 25],
            region=[0, 2, 0, 2, 0, 2],
            projection="X2c",
            frame=["WsNeZ1", "xag", "yag", "zag"],
            zscale=1.5,
        )
        return fig


@pytest.mark.mpl_image_compare
def test_plot3d_ogrgmt_file_multipoint_non_default_style():
    """
    Make sure that non-default style can be set for plotting OGR/GMT file.
    """
    with GMTTempFile(suffix=".gmt") as tmpfile:
        gmt_file = """# @VGMT1.0 @GMULTIPOINT
# @R1/1.5/1/1.5
# FEATURE_DATA
>
1 1 2
1.5 1.5 1"""
        with open(tmpfile.name, "w", encoding="utf8") as file:
            file.write(gmt_file)
        fig = Figure()
        fig.plot3d(
            data=tmpfile.name,
            perspective=[315, 25],
            region=[0, 2, 0, 2, 0, 2],
            projection="X2c",
            frame=["WsNeZ1", "xag", "yag", "zag"],
            zscale=1.5,
            style="c0.2c",
        )
        return fig
