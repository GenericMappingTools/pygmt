"""
Tests grdview.
"""
import pytest
from pygmt import Figure, grdcut, which
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, data_kind


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    Test region as lonmin, lonmax, latmin, latmax.
    """
    return (-116, -109, -47, -44)


@pytest.fixture(scope="module", name="gridfile")
def fixture_gridfile(region):
    """
    Load the NetCDF grid file from the sample earth_relief file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        grdcut(grid="@earth_relief_01d_g", region=region, outgrid=tmpfile.name)
        yield tmpfile.name


@pytest.fixture(scope="module", name="xrgrid")
def fixture_xrgrid(region):
    """
    Load the xarray.DataArray grid from the sample earth_relief file.
    """
    return grdcut(grid="@earth_relief_01d_g", region=region)


@pytest.mark.mpl_image_compare
def test_grdview_grid_dataarray(xrgrid):
    """
    Run grdview by passing in a grid as an xarray.DataArray.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_grid_file_with_region_subset(region):
    """
    Run grdview by passing in a grid filename, and cropping it to a region.
    """
    gridfile = which("@earth_relief_01d_g", download="a")

    fig = Figure()
    fig.grdview(grid=gridfile, region=region)
    return fig


def test_grdview_wrong_kind_of_grid(xrgrid):
    """
    Run grdview using grid input that is not an xarray.DataArray or file.
    """
    dataset = xrgrid.to_dataset()  # convert xarray.DataArray to xarray.Dataset
    assert data_kind(dataset) == "matrix"

    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdview(grid=dataset)


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective(gridfile):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthEast and an elevation angle 15 degrees from the
    z-plane.
    """
    fig = Figure()
    fig.grdview(grid=gridfile, projection="Q15c+", perspective=[135, 15], frame=True)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective_and_zscale(xrgrid):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthWest and an elevation angle 30 degrees from the
    z-plane, plus a z-axis scaling factor of 0.005.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid, perspective=[225, 30], zscale=0.005)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective_and_zsize(xrgrid):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with
    an azimuth from the SouthWest and an elevation angle 30 degrees from the
    z-plane, plus a z-axis size of 10cm.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid, perspective=[225, 30], zsize="10c")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_cmap_for_image_plot(xrgrid):
    """
    Run grdview by passing in a grid and setting a colormap for producing an
    image plot.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid, cmap="oleron", surftype="i")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_cmap_for_surface_monochrome_plot(xrgrid):
    """
    Run grdview by passing in a grid and setting a colormap for producing a
    surface monochrome plot.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid, cmap="oleron", surftype="s+m")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_cmap_for_perspective_surface_plot(xrgrid):
    """
    Run grdview by passing in a grid and setting a colormap for producing a
    surface plot with a 3D perspective viewpoint.
    """
    fig = Figure()
    fig.grdview(
        grid=xrgrid, cmap="oleron", surftype="s", perspective=[225, 30], zscale=0.005
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_on_a_plane(xrgrid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane, while
    setting a 3D perspective viewpoint.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid, plane=-4000, perspective=[225, 30], zscale=0.005)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_on_a_plane_with_colored_frontal_facade(xrgrid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane whose frontal
    facade is colored gray, while setting a 3D perspective viewpoint.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid, plane="-4000+ggray", perspective=[225, 30], zscale=0.005)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective_and_zaxis_frame(xrgrid, region):
    """
    Run grdview by passing in a grid and plotting an annotated vertical z-axis
    frame on a Transverse Mercator (T) projection.
    """
    fig = Figure()
    projection = f"T{(region[0]+region[1])/2}/{abs((region[2]+region[3])/2)}"
    fig.grdview(
        grid=xrgrid,
        projection=projection,
        perspective=[225, 30],
        zscale=0.005,
        frame=["xaf", "yaf", "zaf"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_surface_plot_styled_with_contourpen(xrgrid):
    """
    Run grdview by passing in a grid with styled contour lines plotted on top
    of a surface plot.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid, cmap="relief", surftype="s", contourpen="0.5p,black,dash")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_surface_mesh_plot_styled_with_meshpen(xrgrid):
    """
    Run grdview by passing in a grid with styled mesh lines plotted on top of a
    surface mesh plot.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid, cmap="relief", surftype="sm", meshpen="0.5p,black,dash")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_on_a_plane_styled_with_facadepen(xrgrid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane with styled
    lines for the frontal facade.
    """
    fig = Figure()
    fig.grdview(
        grid=xrgrid,
        plane=-4000,
        perspective=[225, 30],
        zscale=0.005,
        facadepen="0.5p,blue,dash",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_drapegrid_dataarray(xrgrid):
    """
    Run grdview by passing in both a grid and drapegrid as an xarray.DataArray,
    setting a colormap for producing an image plot.
    """
    drapegrid = 1.1 * xrgrid

    fig = Figure()
    fig.grdview(grid=xrgrid, drapegrid=drapegrid, cmap="oleron", surftype="c")
    return fig


def test_grdview_wrong_kind_of_drapegrid(xrgrid):
    """
    Run grdview using drapegrid input that is not an xarray.DataArray or file.
    """
    dataset = xrgrid.to_dataset()  # convert xarray.DataArray to xarray.Dataset
    assert data_kind(dataset) == "matrix"

    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdview(grid=xrgrid, drapegrid=dataset)
