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
def test_grdview_reliefgrid_dataarray(grid):
    """
    Run grdview by passing in a reliefgrid as an xarray.DataArray.
    """
    fig = Figure()
    fig.grdview(reliefgrid=grid)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_reliefgrid_file_with_region_subset():
    """
    Run grdview by passing in a reliefgrid filename, and cropping it to a region.
    """
    gridfile = which("@earth_relief_60m", download="c")

    fig = Figure()
    fig.grdview(reliefgrid=gridfile, region=[-116, -109, -47, -44])
    return fig


def test_grdview_wrong_kind_of_reliefgrid(grid):
    """
    Run grdview using reliefgrid input that is not an xarray.DataArray or file.
    """
    dataset = grid.to_dataset()  # convert xarray.DataArray to xarray.Dataset
    assert data_kind(dataset) == "matrix"

    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdview(reliefgrid=dataset)


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective(grid):
    """
    Run grdview by passing in a reliefgrid and setting a perspective viewpoint with an
    azimuth from the SouthEast and an elevation angle 15 degrees from the z-plane.
    """
    fig = Figure()
    fig.grdview(reliefgrid=grid, perspective=[135, 15])
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective_and_zscale(grid):
    """
    Run grdview by passing in a reliefgrid and setting a perspective viewpoint with an
    azimuth from the SouthWest and an elevation angle 30 degrees from the z-plane, plus
    a z-axis scaling factor of 0.005.
    """
    fig = Figure()
    fig.grdview(reliefgrid=grid, perspective=[225, 30], zscale=0.005)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective_and_zsize(grid):
    """
    Run grdview by passing in a reliefgrid and setting a perspective viewpoint with an
    azimuth from the SouthWest and an elevation angle 30 degrees from the z-plane, plus
    a z-axis size of 10cm.
    """
    fig = Figure()
    fig.grdview(reliefgrid=grid, perspective=[225, 30], zsize="10c")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_cmap_for_image_plot(grid):
    """
    Run grdview by passing in a reliefgrid and setting a colormap for producing an image
    plot.
    """
    fig = Figure()
    fig.grdview(reliefgrid=grid, cmap="oleron", surftype="i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_cmap_for_surface_monochrome_plot(grid):
    """
    Run grdview by passing in a reliefgrid and setting a colormap for producing a
    surface monochrome plot.
    """
    fig = Figure()
    fig.grdview(reliefgrid=grid, cmap="oleron", surftype="s+m")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_cmap_for_perspective_surface_plot(grid):
    """
    Run grdview by passing in a reliefgrid and setting a colormap for producing a
    surface plot with a 3D perspective viewpoint.
    """
    fig = Figure()
    fig.grdview(
        reliefgrid=grid,
        cmap="oleron",
        surftype="s",
        perspective=[225, 30],
        zscale=0.005,
    )
    return fig
