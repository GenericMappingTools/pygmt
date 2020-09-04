"""
Test Figure.grdimage
"""
import numpy as np
import pytest
import xarray as xr

from .. import Figure
from ..datasets import load_earth_relief
from ..exceptions import GMTInvalidInput
from ..helpers.testing import check_figures_equal


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    "Load the grid data from the sample earth_relief file"
    return load_earth_relief(registration="gridline")


@pytest.fixture(scope="module", name="xrgrid")
def fixture_xrgrid():
    """
    Create a sample xarray.DataArray grid for testing
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
    "Plot an image using an xarray grid"
    fig = Figure()
    fig.grdimage(grid, cmap="earth", projection="W0/6i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdimage_slice(grid):
    "Plot an image using an xarray grid that has been sliced"
    grid_ = grid.sel(lat=slice(-30, 30))
    fig = Figure()
    fig.grdimage(grid_, cmap="earth", projection="M6i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdimage_file():
    "Plot an image using file input"
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
def test_grdimage_xarray_shading(grid, fig_ref, fig_test):
    """
    Test that shading works well for xarray.
    See https://github.com/GenericMappingTools/pygmt/issues/364
    """
    fig_ref.grdimage(
        "@earth_relief_01d_g",
        region=[-180, 180, -90, 90],
        frame=True,
        projection="Cyl_stere/6i",
        cmap="geo",
        shading=True,
    )
    fig_test.grdimage(
        grid,
        region=[-180, 180, -90, 90],
        frame=True,
        projection="Cyl_stere/6i",
        cmap="geo",
        shading=True,
    )


def test_grdimage_fails():
    "Should fail for unrecognized input"
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdimage(np.arange(20).reshape((4, 5)))


# This test needs to run first before the other tests (on Linux at least) so
# that a black image isn't plotted due to an `inf` value when resampling.
# See also https://github.com/GenericMappingTools/pygmt/pull/476
@pytest.mark.runfirst
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


@check_figures_equal()
def test_grdimage_central_longitude(grid, fig_ref, fig_test):
    """
    Test that plotting a grid centred at different longitudes/meridians work.
    """
    fig_ref.grdimage("@earth_relief_01d_g", projection="W120/15c", cmap="geo")
    fig_test.grdimage(grid, projection="W120/15c", cmap="geo")
