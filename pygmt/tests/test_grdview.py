"""
Test Figure.grdview.
"""

import pytest
from pygmt import Figure, grdcut
from pygmt.alias import AliasSystem
from pygmt.exceptions import GMTInvalidInput, GMTTypeError
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief
from pygmt.src.grdview import _alias_option_Q


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    Test region as lonmin, lonmax, latmin, latmax.
    """
    return [-55, -50, -18, -12]


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="gridfile")
def fixture_gridfile(grid, region):
    """
    Load the netCDF grid file from the sample earth_relief file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        grdcut(grid=grid, region=region, outgrid=tmpfile.name)
        yield tmpfile.name


@pytest.fixture(scope="module", name="xrgrid")
def fixture_xrgrid(grid, region):
    """
    Load the xarray.DataArray grid from the sample earth_relief file.
    """
    return grdcut(grid=grid, region=region)


def test_grdview_alias_Q():  # noqa: N802
    """
    Test the parameters for the -Q option.
    """

    def alias_wrapper(**kwargs):
        """
        A wrapper function for testing the parameters of -Q option.
        """
        return AliasSystem(Q=_alias_option_Q(**kwargs)).get("Q")

    # Test surftype
    assert alias_wrapper(surftype="surface") == "s"
    assert alias_wrapper(surftype="mesh") == "m"
    assert alias_wrapper(surftype="surface+mesh") == "sm"
    assert alias_wrapper(surftype="waterfall_x") == "mx"
    assert alias_wrapper(surftype="waterfall_y") == "my"
    assert alias_wrapper(surftype="image") == "i"

    assert alias_wrapper(surftype="image", nan_transparent=True) == "c"
    assert alias_wrapper(surftype="image", dpi=150) == "i150"
    assert alias_wrapper(surftype="image", dpi=150, nan_transparent=True) == "c150"

    assert alias_wrapper(surftype="mesh", mesh_fill="blue") == "mblue"
    assert alias_wrapper(surftype="surface", monochrome=True) == "s+m"
    assert alias_wrapper(surftype="surface+mesh", monochrome=True) == "sm+m"


@pytest.mark.mpl_image_compare
def test_grdview_grid_dataarray(xrgrid):
    """
    Run grdview by passing in a grid as an xarray.DataArray.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_surftype(grid):
    """
    Test grdview with different surftype values.
    """
    args = {
        "grid": grid,
        "projection": "M?",
        "frame": True,
        "panel": True,
        "perspective": (-150, 25),
        "zsize": "1.0c",
    }
    fig = Figure()
    with fig.subplot(nrows=2, ncols=3, subsize=(5, 5), margins=(0, -1)):
        fig.grdview(surftype="surface", cmap="SCM/oleron", **args)
        fig.grdview(surftype="surface+mesh", cmap="SCM/oleron", **args)
        fig.grdview(surftype="image", **args)
        fig.grdview(surftype="mesh", **args)
        fig.grdview(surftype="waterfall_x", **args)
        fig.grdview(surftype="waterfall_y", **args)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_image_dpi(grid):
    """
    Test grdview with surftype="image" and dpi parameter.
    """
    fig = Figure()
    for dpi in [None, 10, 100]:
        fig.grdview(
            grid=grid,
            projection="M4c",
            surftype="image",
            dpi=dpi,
            frame=["af", f"WSen+tdpi={dpi}"],
            perspective=(225, 30),
        )
        fig.shift_origin(xshift="7c")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_monochrome(grid):
    """
    Test grdview with different surftype values and monochrome=True.
    """
    args = {
        "grid": grid,
        "projection": "M?",
        "frame": True,
        "panel": True,
        "perspective": (-150, 25),
        "zsize": "1.0c",
        "monochrome": True,
    }
    fig = Figure()
    with fig.subplot(nrows=2, ncols=3, subsize=("5c", "5c"), margins=(0, -0.5)):
        fig.grdview(surftype="surface", cmap="SCM/oleron", **args)
        fig.grdview(surftype="surface+mesh", cmap="SCM/oleron", **args)
        fig.grdview(surftype="mesh", **args)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_mesh_pen_and_mesh_fill(grid):
    """
    Test grdview with mesh_pena and mesh_fill parameters.
    """
    args = {
        "grid": grid,
        "projection": "M?",
        "frame": True,
        "panel": True,
        "perspective": (-150, 25),
        "zsize": "1.0c",
        "mesh_fill": "lightred",
        "mesh_pen": "0.5p,blue",
    }
    fig = Figure()
    with fig.subplot(nrows=1, ncols=3, subsize=("5c", "5c"), margins=0):
        for surftype in ["mesh", "waterfall_x", "waterfall_y"]:
            fig.grdview(surftype=surftype, **args)
    return fig


def test_grdview_wrong_kind_of_grid(xrgrid):
    """
    Run grdview using grid input that is not an xarray.DataArray or file.
    """
    dataset = xrgrid.to_dataset()  # convert xarray.DataArray to xarray.Dataset
    fig = Figure()
    with pytest.raises(GMTTypeError):
        fig.grdview(grid=dataset)


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective(gridfile):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with an azimuth
    from the SouthEast and an elevation angle 15 degrees from the z-plane.
    """
    fig = Figure()
    fig.grdview(grid=gridfile, projection="Q15c+", perspective=[135, 15], frame=True)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective_and_zscale(xrgrid):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with an azimuth
    from the SouthWest and an elevation angle 30 degrees from the z-plane, plus a z-axis
    scaling factor of 0.005.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid, perspective=[225, 30], zscale=0.005)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective_and_zsize(xrgrid):
    """
    Run grdview by passing in a grid and setting a perspective viewpoint with an azimuth
    from the SouthWest and an elevation angle 30 degrees from the z-plane, plus a z-axis
    size of 10cm.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid, perspective=[225, 30], zsize="10c")
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_on_a_plane(xrgrid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane, while setting a 3-D
    perspective viewpoint.
    """
    fig = Figure()
    fig.grdview(grid=xrgrid, plane=100, perspective=[225, 30], zscale=0.005)
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_on_a_plane_with_colored_frontal_facade(xrgrid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane whose frontal facade
    is colored gray, while setting a 3-D perspective viewpoint.
    """
    fig = Figure()
    fig.grdview(
        grid=xrgrid, plane=100, facade_fill="gray", perspective=[225, 30], zscale=0.005
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_with_perspective_and_zaxis_frame(xrgrid, region):
    """
    Run grdview by passing in a grid and plotting an annotated vertical z-axis frame on
    a Transverse Mercator (T) projection.
    """
    fig = Figure()
    projection = f"T{(region[0] + region[1]) / 2}/{abs((region[2] + region[3]) / 2)}"
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
    Run grdview by passing in a grid with styled contour lines plotted on top of a
    surface plot.
    """
    fig = Figure()
    fig.grdview(
        grid=xrgrid,
        cmap="gmt/relief",
        surftype="surface",
        contour_pen="0.5p,black,dashed",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_surface_mesh_plot_styled_with_meshpen(xrgrid):
    """
    Run grdview by passing in a grid with styled mesh lines plotted on top of a surface
    mesh plot.
    """
    fig = Figure()
    fig.grdview(
        grid=xrgrid,
        cmap="gmt/relief",
        surftype="surface+mesh",
        mesh_pen="0.5p,black,dashed",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_on_a_plane_styled_with_facadepen(xrgrid):
    """
    Run grdview by passing in a grid and plotting it on a z-plane with styled lines for
    the frontal facade.
    """
    fig = Figure()
    fig.grdview(
        grid=xrgrid,
        plane=100,
        perspective=[225, 30],
        zscale=0.005,
        facade_pen="0.5p,blue,dashed",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_grdview_facadepen_default_plane(xrgrid):
    """
    Run grdview by passing in a grid and plotting it on the default z-plane with styled
    lines for the frontal facade.
    """
    fig = Figure()
    fig.grdview(
        grid=xrgrid, perspective=[225, 30], zscale=0.005, facade_pen="0.5p,blue,dashed"
    )
    return fig


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_grdview_drapegrid_dataarray(xrgrid):
    """
    Run grdview by passing in both a grid and drape_grid as an xarray.DataArray, setting
    a colormap for producing an image plot.
    """
    drape_grid = 1.1 * xrgrid

    # accessor information are lost during xarray multiplication
    drape_grid.gmt.registration = xrgrid.gmt.registration
    drape_grid.gmt.gtype = xrgrid.gmt.gtype

    fig = Figure()
    fig.grdview(
        grid=xrgrid,
        drape_grid=drape_grid,
        cmap="SCM/oleron",
        surftype="image",
        nan_transparent=True,
        frame=True,
    )
    return fig


def test_grdview_wrong_kind_of_drapegrid(xrgrid):
    """
    Run grdview using drape_grid input that is not an xarray.DataArray or file.
    """
    dataset = xrgrid.to_dataset()  # convert xarray.DataArray to xarray.Dataset
    fig = Figure()
    with pytest.raises(GMTTypeError):
        fig.grdview(grid=xrgrid, drape_grid=dataset)


def test_grdview_invalid_surftype(gridfile):
    """
    Test grdview with an invalid surftype or invalid combination of surftype and other
    parameters.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdview(grid=gridfile, surftype="surface", dpi=300)
    with pytest.raises(GMTInvalidInput):
        fig.grdview(grid=gridfile, surftype="surface", nan_transparent=True)
    with pytest.raises(GMTInvalidInput):
        fig.grdview(grid=gridfile, surftype="surface", mesh_fill="red")


def test_grdview_mixed_syntax(gridfile):
    """
    Run grdview using grid as a file and drapegrid as an xarray.DataArray.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.grdview(grid=gridfile, cmap="SCM/oleron", surftype="i", dpi=300)
    with pytest.raises(GMTInvalidInput):
        fig.grdview(grid=gridfile, cmap="SCM/oleron", surftype="m", mesh_fill="red")
    with pytest.raises(GMTInvalidInput):
        fig.grdview(grid=gridfile, cmap="SCM/oleron", surftype="s", monochrome=True)
    with pytest.raises(GMTInvalidInput):
        fig.grdview(
            grid=gridfile, cmap="SCM/oleron", surftype="i", nan_transparent=True
        )
