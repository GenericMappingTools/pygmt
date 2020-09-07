"""
Tests grdview
"""
import pytest

from .. import Figure, grdcut, which
from ..exceptions import GMTInvalidInput
from ..helpers import GMTTempFile, data_kind
from ..helpers.testing import check_figures_equal


@pytest.fixture(scope="module", name="region")
def fixture_region():
    "Test region as lonmin, lonmax, latmin, latmax"
    return (-116, -109, -47, -44)


@pytest.fixture(scope="module", name="gridfile")
def fixture_gridfile(region):
    """
    Load the NetCDF grid file from the sample earth_relief file
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        grdcut(grid="@earth_relief_01d_g", region=region, outgrid=tmpfile.name)
        yield tmpfile.name


@pytest.fixture(scope="module", name="grid")
def fixture_grid(region):
    """
    Load the xarray.DataArray grid from the sample earth_relief file
    """
    return grdcut(grid="@earth_relief_01d_g", region=region)


@check_figures_equal()
def test_grdview_grid_dataarray(gridfile, grid):
    """
    Run grdview by passing in a grid as an xarray.DataArray.
    """
    fig_ref = Figure()
    fig_ref.grdview(grid=gridfile)
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
def test_grdview_with_perspective(gridfile, grid):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthEast and an elevation angle 15 degrees from the
    z-plane.
    """
    fig_ref = Figure()
    fig_ref.grdview(grid=gridfile, perspective=[135, 15])
    fig_test = Figure()
    fig_test.grdview(grid=grid, perspective=[135, 15])
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_perspective_and_zscale(gridfile, grid):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthWest and an elevation angle 30 degrees from the
    z-plane, plus a z-axis scaling factor of 0.005.
    """
    fig_ref = Figure()
    fig_ref.grdview(grid=gridfile, perspective=[225, 30], zscale=0.005)
    fig_test = Figure()
    fig_test.grdview(grid=grid, perspective=[225, 30], zscale=0.005)
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_perspective_and_zsize(gridfile, grid):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthWest and an elevation angle 30 degrees from the
    z-plane, plus a z-axis size of 10cm.
    """
    fig_ref = Figure()
    fig_ref.grdview(grid=gridfile, perspective=[225, 30], zsize="10c")
    fig_test = Figure()
    fig_test.grdview(grid=grid, perspective=[225, 30], zsize="10c")
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_cmap_for_image_plot(gridfile, grid):
    """
    Run grdview by passing in a grid and setting a colormap for producing an
    image plot.
    """
    fig_ref = Figure()
    fig_ref.grdview(grid=gridfile, cmap="oleron", surftype="i")
    fig_test = Figure()
    fig_test.grdview(grid=grid, cmap="oleron", surftype="i")
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_cmap_for_surface_monochrome_plot(gridfile, grid):
    """
    Run grdview by passing in a grid and setting a colormap for producing a
    surface monochrome plot.
    """
    fig_ref = Figure()
    fig_ref.grdview(grid=gridfile, cmap="oleron", surftype="s+m")
    fig_test = Figure()
    fig_test.grdview(grid=grid, cmap="oleron", surftype="s+m")
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_cmap_for_perspective_surface_plot(gridfile, grid):
    """
    Run grdview by passing in a grid and setting a colormap for producing a
    surface plot with a 3D perspective viewpoint.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid=gridfile, cmap="oleron", surftype="s", perspective=[225, 30], zscale=0.005
    )
    fig_test = Figure()
    fig_test.grdview(
        grid=grid, cmap="oleron", surftype="s", perspective=[225, 30], zscale=0.005
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_on_a_plane(gridfile, grid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane, while
    setting a 3D perspective viewpoint.
    """
    fig_ref = Figure()
    fig_ref.grdview(grid=gridfile, plane=-4000, perspective=[225, 30], zscale=0.005)
    fig_test = Figure()
    fig_test.grdview(grid=grid, plane=-4000, perspective=[225, 30], zscale=0.005)
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_on_a_plane_with_colored_frontal_facade(gridfile, grid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane whose frontal
    facade is colored gray, while setting a 3D perspective viewpoint.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid=gridfile, plane="-4000+ggray", perspective=[225, 30], zscale=0.005
    )
    fig_test = Figure()
    fig_test.grdview(
        grid=grid, plane="-4000+ggray", perspective=[225, 30], zscale=0.005
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_with_perspective_and_zaxis_frame(gridfile, grid):
    """
    Run grdview by passing in a grid and plotting an annotated vertical
    z-axis frame.
    """
    fig_ref = Figure()
    fig_ref.grdview(grid=gridfile, perspective=[225, 30], zscale=0.005, frame="zaf")
    fig_test = Figure()
    fig_test.grdview(grid=grid, perspective=[225, 30], zscale=0.005, frame="zaf")
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_surface_plot_styled_with_contourpen(gridfile, grid):
    """
    Run grdview by passing in a grid with styled contour lines plotted on top
    of a surface plot.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid=gridfile, cmap="relief", surftype="s", contourpen="0.5p,black,dash"
    )
    fig_test = Figure()
    fig_test.grdview(
        grid=grid, cmap="relief", surftype="s", contourpen="0.5p,black,dash"
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_surface_mesh_plot_styled_with_meshpen(gridfile, grid):
    """
    Run grdview by passing in a grid with styled mesh lines plotted on top of a
    surface mesh plot.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid=gridfile, cmap="relief", surftype="sm", meshpen="0.5p,black,dash"
    )
    fig_test = Figure()
    fig_test.grdview(grid=grid, cmap="relief", surftype="sm", meshpen="0.5p,black,dash")
    return fig_ref, fig_test


@check_figures_equal()
def test_grdview_on_a_plane_styled_with_facadepen(gridfile, grid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane with styled
    lines for the frontal facade.
    """
    fig_ref = Figure()
    fig_ref.grdview(
        grid=gridfile,
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
def test_grdview_drapegrid_dataarray(gridfile, grid):
    """
    Run grdview by passing in both a grid and drapegrid as an xarray.DataArray,
    setting a colormap for producing an image plot.
    """
    drapegrid = 1.1 * grid

    fig_ref = Figure()
    fig_ref.grdview(grid=gridfile, drapegrid=drapegrid, cmap="oleron", surftype="c")
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
