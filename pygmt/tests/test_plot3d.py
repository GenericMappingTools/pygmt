"""
Tests plot3d.
"""
import os

import numpy as np
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import check_figures_equal

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


@check_figures_equal()
def test_plot3d_red_circles_zscale(data, region):
    "Plot the 3D data in red circles passing in vectors and setting zscale = 5"
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.plot3d(
        data=POINTS_DATA,
        Jz=5,
        p="225/30",
        R="/".join(map(str, region)),
        J="X4i",
        S="c0.2c",
        G="red",
        B=["afg", "zafg"],
    )
    fig_test.plot3d(
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
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_red_circles_zsize(data, region):
    "Plot the 3D data in red circles passing in vectors and setting zsize = 3i"
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.plot3d(
        data=POINTS_DATA,
        JZ="3i",
        p="225/30",
        R="/".join(map(str, region)),
        J="X4i",
        S="c0.2c",
        G="red",
        B=["afg", "zafg"],
    )
    fig_test.plot3d(
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
    return fig_ref, fig_test


def test_plot3d_fail_no_data(data, region):
    """
    Plot should raise an exception if no data is given.
    """
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


def test_plot3d_fail_size_color(data, region):
    """
    Should raise an exception if array sizes and color are used with matrix.
    """
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


@check_figures_equal()
def test_plot3d_projection(data, region):
    """
    Plot the data in green squares with a projection.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.plot3d(
        data=POINTS_DATA,
        Jz=5,
        p="225/30",
        R="/".join(map(str, region)),
        J="R270/4i",
        S="s1c",
        G="green",
        B=["ag", "zag"],
    )
    fig_test.plot3d(
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
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_colors(data, region):
    """
    Plot the data using z as colors.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.plot3d(
        data=POINTS_DATA,
        Jz=5,
        p="225/30",
        G="+z",
        R="/".join(map(str, region)),
        J="X3i",
        S="c0.5c",
        C="cubhelix",
        B=["afg", "zafg"],
        i="0,1,2,2",
    )
    fig_test.plot3d(
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
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_sizes(data, region):
    """
    Plot the data using z as sizes.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.plot3d(
        data=POINTS_DATA,
        Jz=5,
        p="225/30",
        i="0,1,2,2+s0.5",
        R="/".join(map(str, region)),
        J="X4i",
        S="ui",
        G="blue",
        B=["af", "zaf"],
    )
    fig_test.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        sizes=0.5 * data[:, 2],
        region=region,
        projection="X4i",
        # Using inches instead of cm because of upstream bug at
        # https://github.com/GenericMappingTools/gmt/issues/4386
        style="ui",
        color="blue",
        frame=["af", "zaf"],
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_colors_sizes(data, region):
    """
    Plot the data using z as sizes and colors.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.plot3d(
        data=POINTS_DATA,
        Jz=5,
        p="225/30",
        i="0,1,2,2,2+s0.5",
        R="/".join(map(str, region)),
        J="X3i",
        S="ui",
        C="copper",
        B=["af", "zaf"],
    )
    fig_test.plot3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        zscale=5,
        perspective=[225, 30],
        color=data[:, 2],
        sizes=0.5 * data[:, 2],
        region=region,
        projection="X3i",
        # Using inches instead of cm because of upstream bug at
        # https://github.com/GenericMappingTools/gmt/issues/4386
        style="ui",
        cmap="copper",
        frame=["af", "zaf"],
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_colors_sizes_proj(data, region):
    """
    Plot the data using z as sizes and colors with a projection.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.plot3d(
        data=POINTS_DATA,
        Jz=5,
        p="225/30",
        R="/".join(map(str, region)),
        J="M10i",
        B=["af", "zaf"],
        G="+z",
        i="0,1,2,2,2+s1",
        S="ui",
        C="copper",
    )
    fig_test.plot3d(
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
        # Using inches instead of cm because of upstream bug at
        # https://github.com/GenericMappingTools/gmt/issues/4386
        style="ui",
        cmap="copper",
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_transparency():
    """
    Plot the data with a constant transparency.
    """
    x = np.arange(1, 10)
    y = np.arange(1, 10)
    z = np.arange(1, 10) * 10

    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    with GMTTempFile() as tmpfile:
        np.savetxt(tmpfile.name, np.c_[x, y, z], fmt="%d")
        fig_ref.plot3d(
            data=tmpfile.name,
            S="u0.2c",
            G="blue",
            R="0/10/0/10/10/90",
            J="X4i",
            Jz=0.1,
            B="",
            p="135/30",
            t=80.0,
        )

    fig_test.plot3d(
        x=x,
        y=y,
        z=z,
        style="u0.2c",
        color="blue",
        region=[0, 10, 0, 10, 10, 90],
        projection="X4i",
        zscale=0.1,
        frame=True,
        perspective=[135, 30],
        transparency=80.0,
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_varying_transparency():
    """
    Plot the data using z as transparency using 3-D column symbols.
    """
    x = np.arange(1, 10)
    y = np.arange(1, 10)
    z = np.arange(1, 10) * 10

    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    with GMTTempFile() as tmpfile:
        np.savetxt(tmpfile.name, np.c_[x, y, z, z, z], fmt="%d")
        fig_ref.plot3d(
            data=tmpfile.name,
            S="o0.2c+B5",
            G="blue",
            R="0/10/0/10/10/90",
            J="X4i",
            Jz=0.1,
            B="",
            p="135/30",
            t="",
        )
    fig_test.plot3d(
        x=x,
        y=y,
        z=z,
        style="o0.2c+B5",
        color="blue",
        region=[0, 10, 0, 10, 10, 90],
        projection="X4i",
        zscale=0.1,
        frame=True,
        perspective=[135, 30],
        transparency=z,
    )
    return fig_ref, fig_test


@check_figures_equal()
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

    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    with GMTTempFile() as tmpfile:
        np.savetxt(tmpfile.name, np.c_[x, y, z, color, size, transparency])
        fig_ref.plot3d(
            data=tmpfile.name,
            R="0/10/0/10/10/90",
            J="X4i",
            Jz=0.1,
            p="135/30",
            B="",
            S="uc",
            C="gray",
            t="",
        )
    fig_test.plot3d(
        x=x,
        y=y,
        z=z,
        region=[0, 10, 0, 10, 10, 90],
        projection="X4i",
        zscale=0.1,
        perspective=[135, 30],
        frame=True,
        style="uc",
        color=color,
        sizes=size,
        cmap="gray",
        transparency=transparency,
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_matrix(data, region):
    """
    Plot the data passing in a matrix and specifying columns.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.plot3d(
        data=POINTS_DATA,
        Jz=5,
        p="225/30",
        R="/".join(map(str, region)),
        J="M10i",
        S="c1c",
        G="#aaaaaa",
        B=["a", "za"],
        i="0,1,2",
    )
    fig_test.plot3d(
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
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_matrix_color(data, region):
    """
    Plot the data passing in a matrix and using a colormap.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.plot3d(
        data=POINTS_DATA,
        Jz=5,
        p="225/30",
        R="/".join(map(str, region)),
        J="X5i",
        S="c0.5c",
        C="rainbow",
        i="0,1,2,2",
        B=["a", "za"],
    )
    fig_test.plot3d(
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
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_from_file(region):
    """
    Plot using the data file name instead of loaded data.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.plot3d(
        data=POINTS_DATA,
        Jz=5,
        p="225/30",
        R="/".join(map(str, region)),
        J="X10i",
        S="d1c",
        G="yellow",
        B=["af", "zaf"],
        i="0,1,2",
    )
    fig_test.plot3d(
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
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_vectors():
    """
    Plot vectors.
    """
    azimuth = np.array([0, 45, 90, 135, 180, 225, 270, 310])
    lengths = np.linspace(0.1, 1, len(azimuth))
    lon = np.sin(np.deg2rad(azimuth))
    lat = np.cos(np.deg2rad(azimuth))
    elev = np.tan(np.deg2rad(azimuth))
    fig_ref, fig_test = Figure(), Figure()
    with GMTTempFile() as tmpfile:
        np.savetxt(tmpfile.name, np.c_[lon, lat, elev, azimuth, lengths])
        fig_ref.plot3d(
            data=tmpfile.name,
            Jz=2,
            p="225/30",
            R="-2/2/-2/2/-2/2",
            J="X4i",
            S="V1c+e",
            G="black",
            B=["af", "zaf"],
        )
    fig_test.plot3d(
        x=lon,
        y=lat,
        z=elev,
        zscale=2,
        perspective=[225, 30],
        direction=(azimuth, lengths),
        region=[-2, 2, -2, 2, -2, 2],
        projection="X4i",
        style="V1c+e",
        color="black",
        frame=["af", "zaf"],
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_plot3d_scalar_xyz():
    """
    Plot symbols given scalar x, y, z coordinates.
    """
    fig_ref, fig_test = Figure(), Figure()
    with GMTTempFile() as tmpfile:
        np.savetxt(tmpfile.name, np.c_[[-1.5, 0, 1.5], [1.5, 0, -1.5], [-1.5, 0, 1.5]])
        fig_ref.basemap(
            R="-2/2/-2/2/-2/2", B=["xaf+lx", "yaf+ly", "zaf+lz"], Jz=2, p="225/30"
        )
        fig_ref.plot3d(data=tmpfile.name, S="c1c", G="red", Jz="", p="", qi=0)
        fig_ref.plot3d(data=tmpfile.name, S="t1c", G="green", Jz="", p="", qi=1)
        fig_ref.plot3d(data=tmpfile.name, S="s1c", G="blue", Jz="", p="", qi=2)

    fig_test.basemap(
        region=[-2, 2, -2, 2, -2, 2],
        frame=["xaf+lx", "yaf+ly", "zaf+lz"],
        zscale=2,
        perspective=[225, 30],
    )
    fig_test.plot3d(
        x=-1.5, y=1.5, z=-1.5, style="c1c", color="red", zscale=True, perspective=True
    )
    fig_test.plot3d(
        x=0, y=0, z=0, style="t1c", color="green", zscale=True, perspective=True
    )
    fig_test.plot3d(
        x=1.5, y=-1.5, z=1.5, style="s1c", color="blue", zscale=True, perspective=True
    )
    return fig_ref, fig_test
