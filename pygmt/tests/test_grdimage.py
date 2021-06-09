"""
Test Figure.grdimage.
"""
import numpy as np
import pytest
import xarray as xr
from pygmt import Figure
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.testing import check_figures_equal


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(registration="gridline")


@pytest.fixture(scope="module", name="grid_360")
def fixture_grid_360(grid):
    """
    Earth relief grid with longitude range from 0 to 360 (instead of -180 to
    180).
    """
    _grid = grid.copy()  # get a copy of original earth_relief grid
    _grid.encoding.pop("source")  # unlink earth_relief NetCDF source
    _grid["lon"] = np.arange(0, 361, 1)  # convert longitude from -180:180 to 0:360
    return _grid


@pytest.fixture(scope="module", name="xrgrid")
def fixture_xrgrid():
    """
    Create a sample xarray.DataArray grid for testing.
    """
    longitude = np.arange(0, 360, 1)
    latitude = np.arange(-89, 90, 1)
    x = np.sin(np.deg2rad(longitude))
    y = np.linspace(start=0, stop=1, num=179)
    data = y[:, np.newaxis] * x

    return xr.DataArray(
        data,
        coords=[
            ("latitude", latitude, {"units": "degrees_north"}),
            ("longitude", longitude, {"units": "degrees_east"}),
        ],
        attrs={"actual_range": [-1, 1]},
    )


@pytest.mark.mpl_image_compare
def test_grdimage(grid):
    """
    Plot an image using an xarray grid.
    """
    fig = Figure()
    fig.grdimage(grid, cmap="earth", projection="W0/6i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdimage_slice(grid):
    """
    Plot an image using an xarray grid that has been sliced.
    """
    grid_ = grid.sel(lat=slice(-30, 30))
    fig = Figure()
    fig.grdimage(grid_, cmap="earth", projection="M6i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdimage_file():
    """
    Plot an image using file input.
    """
    fig = Figure()
    fig.grdimage(
        "@earth_relief_01d_g",
        cmap="ocean",
        region=[-180, 180, -70, 70],
        projection="W0/10i",
        shading=True,
    )
    return fig


@check_figures_equal()
@pytest.mark.parametrize(
    "shading",
    [True, 0.5, "+a30+nt0.8", "@earth_relief_01d_g+d", "@earth_relief_01d_g+a60+nt0.8"],
)
def test_grdimage_shading_xarray(grid, shading):
    """
    Test that shading works well for xarray.

    The ``shading`` can be True, a constant intensity, some modifiers, or
    a grid with modifiers.

    See https://github.com/GenericMappingTools/pygmt/issues/364 and
    https://github.com/GenericMappingTools/pygmt/issues/618.
    """
    fig_ref, fig_test = Figure(), Figure()
    kwargs = dict(
        region=[-180, 180, -90, 90],
        frame=True,
        projection="Cyl_stere/6i",
        cmap="geo",
        shading=shading,
    )

    fig_ref.grdimage("@earth_relief_01d_g", **kwargs)
    fig_test.grdimage(grid, **kwargs)
    return fig_ref, fig_test


@pytest.mark.xfail(
    reason="Incorrect scaling of geo CPT on xarray.DataArray grdimage plot."
    "See https://github.com/GenericMappingTools/gmt/issues/5294",
)
@check_figures_equal()
def test_grdimage_grid_and_shading_with_xarray(grid, xrgrid):
    """
    Test that shading works well when xarray.DataArray is input to both the
    ``grid`` and ``shading`` arguments.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.grdimage(
        grid="@earth_relief_01d_g", region="GL", cmap="geo", shading=xrgrid, verbose="i"
    )
    fig_ref.colorbar()
    fig_test.grdimage(grid=grid, region="GL", cmap="geo", shading=xrgrid, verbose="i")
    fig_test.colorbar()
    return fig_ref, fig_test


def test_grdimage_fails():
    """
    Should fail for unrecognized input.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdimage(np.arange(20).reshape((4, 5)))


@pytest.mark.mpl_image_compare
def test_grdimage_over_dateline(xrgrid):
    """
    Ensure no gaps are plotted over the 180 degree international dateline.

    Specifically checking that `xrgrid.gmt.gtype = 1` sets `GMT_GRID_IS_GEO`,
    and that `xrgrid.gmt.registration = 0` sets `GMT_GRID_NODE_REG`. Note that
    there would be a gap over the dateline if a pixel registered grid is used.
    See also https://github.com/GenericMappingTools/pygmt/issues/375.
    """
    fig = Figure()
    assert xrgrid.gmt.registration == 0  # gridline registration
    xrgrid.gmt.gtype = 1  # geographic coordinate system
    fig.grdimage(grid=xrgrid, region="g", projection="A0/0/1c", V="i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdimage_global_subset(grid_360):
    """
    Ensure subsets of grids are plotted correctly on a global map.

    Specifically checking that xarray.DataArray grids can wrap around the left
    and right sides on a Mollweide projection (W) plot correctly. Note that a
    Cartesian grid is used here instead of a Geographic grid (i.e.
    GMT_GRID_IS_CARTESIAN). This is a regression test for
    https://github.com/GenericMappingTools/pygmt/issues/732.
    """
    # Get a slice of South America and Africa only (lat=-90:31, lon=-180:41)
    sliced_grid = grid_360[0:121, 0:221]
    assert sliced_grid.gmt.registration == 0  # gridline registration
    assert sliced_grid.gmt.gtype == 0  # Cartesian coordinate system

    fig = Figure()
    fig.grdimage(
        grid=sliced_grid, cmap="vik", region="g", projection="W0/3.5c", frame=True
    )
    return fig


@check_figures_equal()
@pytest.mark.parametrize("lon0", [0, 123, 180])
@pytest.mark.parametrize("proj_type", ["H", "W"])
def test_grdimage_central_meridians(grid, proj_type, lon0):
    """
    Test that plotting a grid with different central meridians (lon0) using
    Hammer (H) and Mollweide (W) projection systems work.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.grdimage(
        "@earth_relief_01d_g", projection=f"{proj_type}{lon0}/15c", cmap="geo"
    )
    fig_test.grdimage(grid, projection=f"{proj_type}{lon0}/15c", cmap="geo")
    return fig_ref, fig_test


# Cylindrical Equidistant (Q) projections plotted with xarray and NetCDF grids
# are still slightly different with an RMS error of 25, see issue at
# https://github.com/GenericMappingTools/pygmt/issues/390
# TO-DO remove tol=1.5 and pytest.mark.xfail once bug is solved in upstream GMT
@check_figures_equal(tol=1.5)
@pytest.mark.parametrize("lat0", [0, 30])
@pytest.mark.parametrize("lon0", [0, 123, 180])
@pytest.mark.parametrize("proj_type", [pytest.param("Q", marks=pytest.mark.xfail), "S"])
def test_grdimage_central_meridians_and_standard_parallels(grid, proj_type, lon0, lat0):
    """
    Test that plotting a grid with different central meridians (lon0) and
    standard_parallels (lat0) using Cylindrical Equidistant (Q) and General
    Stereographic (S) projection systems work.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.grdimage(
        "@earth_relief_01d_g", projection=f"{proj_type}{lon0}/{lat0}/15c", cmap="geo"
    )
    fig_test.grdimage(grid, projection=f"{proj_type}{lon0}/{lat0}/15c", cmap="geo")
    return fig_ref, fig_test
