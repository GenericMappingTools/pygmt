"""
Tests grdview
"""
import pytest

from .. import Figure, which
from ..datasets import load_earth_relief
from ..exceptions import GMTInvalidInput
from ..helpers import data_kind
from ..helpers.testing import check_figures_equal


@pytest.fixture(scope="module", name="region")
def fixture_region():
    "Test region as lonmin, lonmax, latmin, latmax"
    return (-116, -109, -47, -44)


@pytest.fixture(scope="module", name="grid")
def fixture_grid(region):
    "Load the grid data from the sample earth_relief file"
    return load_earth_relief(registration="gridline").sel(
        lat=slice(region[2], region[3]), lon=slice(region[0], region[1])
    )


@check_figures_equal()
def test_grdview_grid_dataarray(grid, region):
    """
    Run grdview by passing in a grid as an xarray.DataArray.
    """
    fig_ref = Figure()
    fig_ref.grdview(grid="@earth_relief_01d_g", region=region)
    fig_test = Figure()
    fig_test.grdview(grid=grid)
    return fig_ref, fig_test


@pytest.mark.mpl_image_compare
def test_grdview_grid_file_with_region_subset(region):
    """
    Run grdview by passing in a grid filename, and cropping it to a region.
    """
    gridfile = which("@earth_relief_01d_g", download="a")

    fig = Figure()
    fig.grdview(grid=gridfile, region=region)
    return fig


def test_grdview_wrong_kind_of_grid(grid):
    """
    Run grdview using grid input that is not an xarray.DataArray or file.
    """
    dataset = grid.to_dataset()  # convert xarray.DataArray to xarray.Dataset
    assert data_kind(dataset) == "matrix"

    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdview(grid=dataset)


@check_figures_equal()
def test_grdview_with_perspective(grid, region):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthEast and an elevation angle 15 degrees from the
    z-plane.
    """
    fig_ref = Figure()
    fig_ref.grdview(grid="@earth_relief_01d_g", region=region, perspective=[135, 15])
    fig_test = Figure()
    fig_test.grdview(grid=grid, perspective=[135, 15])
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_perspective_and_zscale(grid, region):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthWest and an elevation angle 30 degrees from the
    z-plane, plus a z-axis scaling factor of 0.005.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g", region=region, perspective=[225, 30], zscale=0.005
    )
    fig_test = Figure()
    fig_test.grdview(grid=grid, perspective=[225, 30], zscale=0.005)
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_perspective_and_zsize(grid, region):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthWest and an elevation angle 30 degrees from the
    z-plane, plus a z-axis size of 10cm.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g", region=region, perspective=[225, 30], zsize="10c"
    )
    fig_test = Figure()
    fig_test.grdview(grid=grid, perspective=[225, 30], zsize="10c")
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_cmap_for_image_plot(grid, region):
    """
    Run grdview by passing in a grid and setting a colormap for producing an
    image plot.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g", region=region, cmap="oleron", surftype="i"
    )
    fig_test = Figure()
    fig_test.grdview(grid=grid, cmap="oleron", surftype="i")
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_cmap_for_surface_monochrome_plot(grid, region):
    """
    Run grdview by passing in a grid and setting a colormap for producing a
    surface monochrome plot.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g", region=region, cmap="oleron", surftype="s+m"
    )
    fig_test = Figure()
    fig_test.grdview(grid=grid, cmap="oleron", surftype="s+m")
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_cmap_for_perspective_surface_plot(grid, region):
    """
    Run grdview by passing in a grid and setting a colormap for producing a
    surface plot with a 3D perspective viewpoint.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g",
        region=region,
        cmap="oleron",
        surftype="s",
        perspective=[225, 30],
        zscale=0.005,
    )
    fig_test = Figure()
    fig_test.grdview(
        grid=grid, cmap="oleron", surftype="s", perspective=[225, 30], zscale=0.005
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_on_a_plane(grid, region):
    """
    Run grdview by passing in a grid and plotting it on a z-plane, while
    setting a 3D perspective viewpoint.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g",
        region=region,
        plane=-4000,
        perspective=[225, 30],
        zscale=0.005,
    )
    fig_test = Figure()
    fig_test.grdview(grid=grid, plane=-4000, perspective=[225, 30], zscale=0.005)
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_on_a_plane_with_colored_frontal_facade(grid, region):
    """
    Run grdview by passing in a grid and plotting it on a z-plane whose frontal
    facade is colored gray, while setting a 3D perspective viewpoint.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g",
        region=region,
        plane="-4000+ggray",
        perspective=[225, 30],
        zscale=0.005,
    )
    fig_test = Figure()
    fig_test.grdview(
        grid=grid, plane="-4000+ggray", perspective=[225, 30], zscale=0.005
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_perspective_and_zaxis_frame(grid, region):
    """
    Run grdview by passing in a grid and plotting an annotated vertical
    z-axis frame.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g",
        region=region,
        perspective=[225, 30],
        zscale=0.005,
        frame="zaf",
    )
    fig_test = Figure()
    fig_test.grdview(grid=grid, perspective=[225, 30], zscale=0.005, frame="zaf")
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_surface_plot_styled_with_contourpen(grid, region):
    """
    Run grdview by passing in a grid with styled contour lines plotted on top
    of a surface plot.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g",
        region=region,
        cmap="relief",
        surftype="s",
        contourpen="0.5p,black,dash",
    )
    fig_test = Figure()
    fig_test.grdview(
        grid=grid, cmap="relief", surftype="s", contourpen="0.5p,black,dash"
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_surface_mesh_plot_styled_with_meshpen(grid, region):
    """
    Run grdview by passing in a grid with styled mesh lines plotted on top of a
    surface mesh plot.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g",
        region=region,
        cmap="relief",
        surftype="sm",
        meshpen="0.5p,black,dash",
    )
    fig_test = Figure()
    fig_test.grdview(grid=grid, cmap="relief", surftype="sm", meshpen="0.5p,black,dash")
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_on_a_plane_styled_with_facadepen(grid, region):
    """
    Run grdview by passing in a grid and plotting it on a z-plane with styled
    lines for the frontal facade.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g",
        region=region,
        plane=-4000,
        perspective=[225, 30],
        zscale=0.005,
        facadepen="0.5p,blue,dash",
    )
    fig_test = Figure()
    fig_test.grdview(
        grid=grid,
        plane=-4000,
        perspective=[225, 30],
        zscale=0.005,
        facadepen="0.5p,blue,dash",
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_drapegrid_dataarray(grid, region):
    """
    Run grdview by passing in both a grid and drapegrid as an xarray.DataArray,
    setting a colormap for producing an image plot.
    """
    drapegrid = 1.1 * grid

    fig_ref = Figure()
    fig_ref.grdview(
        grid="@earth_relief_01d_g",
        region=region,
        drapegrid=drapegrid,
        cmap="oleron",
        surftype="c",
    )
    fig_test = Figure()
    fig_test.grdview(grid=grid, drapegrid=drapegrid, cmap="oleron", surftype="c")
    return fig_ref, fig_test


def test_grdview_wrong_kind_of_drapegrid(grid):
    """
    Run grdview using drapegrid input that is not an xarray.DataArray or file.
    """
    dataset = grid.to_dataset()  # convert xarray.DataArray to xarray.Dataset
    assert data_kind(dataset) == "matrix"

    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdview(grid=grid, drapegrid=dataset)
