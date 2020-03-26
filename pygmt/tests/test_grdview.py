# pylint: disable=redefined-outer-name
"""
Tests grdview
"""
import pytest

from .. import Figure, which
from ..datasets import load_earth_relief
from ..exceptions import GMTInvalidInput
from ..helpers import data_kind


@pytest.fixture(scope="module")
def grid():
    "Load the grid data from the sample earth_relief file"
    return load_earth_relief().sel(lat=slice(-49, -42), lon=slice(-118, -107))


@pytest.mark.mpl_image_compare
def test_grdview_grid_dataarray(grid):
    """
    Run grdview by passing in a grid as an xarray.DataArray.
    """
    fig = Figure()
    fig.grdview(grid=grid)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_grid_file_with_region_subset():
    """
    Run grdview by passing in a grid filename, and cropping it to a region.
    """
    gridfile = which("@earth_relief_60m", download="c")

    fig = Figure()
    fig.grdview(grid=gridfile, region=[-116, -109, -47, -44])
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


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective(grid):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthEast and an elevation angle 15 degrees from the
    z-plane.
    """
    fig = Figure()
    fig.grdview(grid=grid, perspective=[135, 15])
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective_and_zscale(grid):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthWest and an elevation angle 30 degrees from the
    z-plane, plus a z-axis scaling factor of 0.005.
    """
    fig = Figure()
    fig.grdview(grid=grid, perspective=[225, 30], zscale=0.005)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective_and_zsize(grid):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthWest and an elevation angle 30 degrees from the
    z-plane, plus a z-axis size of 10cm.
    """
    fig = Figure()
    fig.grdview(grid=grid, perspective=[225, 30], zsize="10c")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_cmap_for_image_plot(grid):
    """
    Run grdview by passing in a grid and setting a colormap for producing an
    image plot.
    """
    fig = Figure()
    fig.grdview(grid=grid, cmap="oleron", surftype="i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_cmap_for_surface_monochrome_plot(grid):
    """
    Run grdview by passing in a grid and setting a colormap for producing a
    surface monochrome plot.
    """
    fig = Figure()
    fig.grdview(grid=grid, cmap="oleron", surftype="s+m")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_cmap_for_perspective_surface_plot(grid):
    """
    Run grdview by passing in a grid and setting a colormap for producing a
    surface plot with a 3D perspective viewpoint.
    """
    fig = Figure()
    fig.grdview(
        grid=grid, cmap="oleron", surftype="s", perspective=[225, 30], zscale=0.005,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_on_a_plane(grid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane, while
    setting a 3D perspective viewpoint.
    """
    fig = Figure()
    fig.grdview(grid=grid, plane=-4000, perspective=[225, 30], zscale=0.005)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_on_a_plane_with_colored_frontal_facade(grid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane whose frontal
    facade is colored gray, while setting a 3D perspective viewpoint.
    """
    fig = Figure()
    fig.grdview(grid=grid, plane="-4000+ggray", perspective=[225, 30], zscale=0.005)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective_and_zaxis_frame(grid):
    """
    Run grdview by passing in a grid and plotting an annotated vertical
    z-axis frame.
    """
    fig = Figure()
    fig.grdview(grid=grid, perspective=[225, 30], zscale=0.005, frame="zaf")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_surface_plot_styled_with_contourpen(grid):
    """
    Run grdview by passing in a grid with styled contour lines plotted on top
    of a surface plot.
    """
    fig = Figure()
    fig.grdview(grid=grid, cmap="relief", surftype="s", contourpen="0.5p,black,dash")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_surface_mesh_plot_styled_with_meshpen(grid):
    """
    Run grdview by passing in a grid with styled mesh lines plotted on top of a
    surface mesh plot.
    """
    fig = Figure()
    fig.grdview(grid=grid, cmap="relief", surftype="sm", meshpen="0.5p,black,dash")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_on_a_plane_styled_with_facadepen(grid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane with styled
    lines for the frontal facade.
    """
    fig = Figure()
    fig.grdview(
        grid=grid,
        plane=-4000,
        perspective=[225, 30],
        zscale=0.005,
        facadepen="0.5p,blue,dash",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_drapegrid_dataarray(grid):
    """
    Run grdview by passing in both a grid and drapegrid as an xarray.DataArray,
    setting a colormap for producing an image plot.
    """
    drapegrid = 1.1 * grid

    fig = Figure()
    fig.grdview(grid=grid, drapegrid=drapegrid, cmap="oleron", surftype="c")
    return fig


def test_grdview_wrong_kind_of_drapegrid(grid):
    """
    Run grdview using drapegrid input that is not an xarray.DataArray or file.
    """
    dataset = grid.to_dataset()  # convert xarray.DataArray to xarray.Dataset
    assert data_kind(dataset) == "matrix"

    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdview(grid=grid, drapegrid=dataset)
