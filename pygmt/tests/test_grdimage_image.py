"""
Test Figure.grdimage on 3-band RGB images.
"""
import pytest
from pygmt import Figure, which

rioxarray = pytest.importorskip("rioxarray")


@pytest.fixture(scope="module", name="xr_image")
def fixture_xr_image():
    """
    Load the image data from Blue Marble as an xarray.DataArray with shape {"band": 3,
    "y": 180, "x": 360}.
    """
    geotiff = which(fname="@earth_day_01d_p", download="c")
    with rioxarray.open_rasterio(filename=geotiff) as rda:
        if len(rda.band) == 3:
            xr_image = rda.load()
        assert xr_image.sizes == {"band": 3, "y": 180, "x": 360}
        return xr_image


@pytest.mark.mpl_image_compare
def test_grdimage_image():
    """
    Plot a 3-band RGB image using file input.
    """
    fig = Figure()
    fig.grdimage(grid="@earth_day_01d")
    return fig


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare(filename="test_grdimage_image.png")
def test_grdimage_image_dataarray(xr_image):
    """
    Plot a 3-band RGB image using xarray.DataArray input.
    """
    fig = Figure()
    fig.grdimage(grid=xr_image)
    return fig


@pytest.mark.parametrize(
    "dtype",
    ["int8", "uint16", "int16", "uint32", "int32", "float32", "float64"],
)
def test_grdimage_image_dataarray_unsupported_dtype(dtype, xr_image):
    """
    Plot a 3-band RGB image using xarray.DataArray input, with an unsupported data type.
    """
    fig = Figure()
    image = xr_image.copy().astype(dtype=dtype)
    with pytest.warns(expected_warning=RuntimeWarning) as record:
        fig.grdimage(grid=image)
        assert len(record) == 1
