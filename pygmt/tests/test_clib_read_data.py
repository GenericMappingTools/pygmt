"""
Test the Session.read_data method.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTCLibError
from pygmt.helpers import GMTTempFile
from pygmt.io import load_dataarray
from pygmt.src import which

try:
    import rioxarray

    _HAS_RIOXARRAY = True
except ImportError:
    _HAS_RIOXARRAY = False


@pytest.fixture(scope="module", name="expected_xrgrid")
def fixture_expected_xrgrid():
    """
    The expected xr.DataArray object for the static_earth_relief.nc file.
    """
    return load_dataarray(which("@static_earth_relief.nc"))


@pytest.fixture(scope="module", name="expected_xrimage")
def fixture_expected_xrimage():
    """
    The expected xr.DataArray object for the @earth_day_01d file.
    """
    if _HAS_RIOXARRAY:
        with rioxarray.open_rasterio(which("@earth_day_01d")) as da:
            dataarray = da.load().drop_vars("spatial_ref")
            return dataarray
    return None


def test_clib_read_data_dataset():
    """
    Test the Session.read_data method for datasets.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        # Prepare the sample data file
        with Path(tmpfile.name).open(mode="w", encoding="utf-8") as fp:
            print("# x y z name", file=fp)
            print(">", file=fp)
            print("1.0 2.0 3.0 TEXT1 TEXT23", file=fp)
            print("4.0 5.0 6.0 TEXT4 TEXT567", file=fp)
            print(">", file=fp)
            print("7.0 8.0 9.0 TEXT8 TEXT90", file=fp)
            print("10.0 11.0 12.0 TEXT123 TEXT456789", file=fp)

        with Session() as lib:
            ds = lib.read_data(tmpfile.name, kind="dataset").contents
            df = ds.to_dataframe(header=0)
            expected_df = pd.DataFrame(
                data={
                    "x": [1.0, 4.0, 7.0, 10.0],
                    "y": [2.0, 5.0, 8.0, 11.0],
                    "z": [3.0, 6.0, 9.0, 12.0],
                    "name": pd.Series(
                        [
                            "TEXT1 TEXT23",
                            "TEXT4 TEXT567",
                            "TEXT8 TEXT90",
                            "TEXT123 TEXT456789",
                        ],
                        dtype=pd.StringDtype(),
                    ),
                }
            )
            pd.testing.assert_frame_equal(df, expected_df)


def test_clib_read_data_grid(expected_xrgrid):
    """
    Test the Session.read_data method for grids.
    """
    with Session() as lib:
        grid = lib.read_data("@static_earth_relief.nc", kind="grid").contents
        xrgrid = grid.to_dataarray()
        xr.testing.assert_equal(xrgrid, expected_xrgrid)
        assert grid.header.contents.n_bands == 1  # Explicitly check n_bands


def test_clib_read_data_grid_two_steps(expected_xrgrid):
    """
    Test the Session.read_data method for grids in two steps, first reading the header
    and then the data.
    """
    infile = "@static_earth_relief.nc"
    with Session() as lib:
        # Read the header first
        data_ptr = lib.read_data(infile, kind="grid", mode="GMT_CONTAINER_ONLY")
        grid = data_ptr.contents
        header = grid.header.contents
        assert header.n_rows == 14
        assert header.n_columns == 8
        assert header.wesn[:] == [-55.0, -47.0, -24.0, -10.0]
        assert header.z_min == 190.0
        assert header.z_max == 981.0
        assert header.n_bands == 1  # Explicitly check n_bands
        assert not grid.data  # The data is not read yet

        # Read the data
        lib.read_data(infile, kind="grid", mode="GMT_DATA_ONLY", data=data_ptr)

        # Full check
        xrgrid = data_ptr.contents.to_dataarray()
        xr.testing.assert_equal(xrgrid, expected_xrgrid)


def test_clib_read_data_grid_actual_image(expected_xrimage):
    """
    Test the Session.read_data method for grid, but actually the file is an image.
    """
    with Session() as lib:
        image = lib.read_data("@earth_day_01d", kind="grid").contents
        # Explicitly check n_bands. Only one band is read for 3-band images.
        assert image.header.contents.n_bands == 1

        xrimage = image.to_dataarray()
        assert xrimage.shape == (180, 360)
        assert xrimage.coords["x"].data.min() == -179.5
        assert xrimage.coords["x"].data.max() == 179.5
        assert xrimage.coords["y"].data.min() == -89.5
        assert xrimage.coords["y"].data.max() == 89.5
        assert xrimage.data.min() == 10.0
        assert xrimage.data.max() == 255.0
        # Data are stored as uint8 in images but are converted to float32 when reading
        # into a GMT_GRID container.
        assert xrimage.data.dtype == np.float32

        if _HAS_RIOXARRAY:  # Full check if rioxarray is installed.
            assert expected_xrimage.band.size == 3  # 3-band image.
            xr.testing.assert_equal(
                xrimage,
                expected_xrimage.isel(band=0).drop_vars(["band"]).sortby("y"),
            )


def test_clib_read_data_image(expected_xrimage):
    """
    Test the Session.read_data method for images.
    """
    with Session() as lib:
        image = lib.read_data("@earth_day_01d", kind="image").contents

        xrimage = image.to_dataarray()
        assert xrimage.shape == (3, 180, 360)
        assert xrimage.coords["x"].data.min() == -179.5
        assert xrimage.coords["x"].data.max() == 179.5
        assert xrimage.coords["y"].data.min() == -89.5
        assert xrimage.coords["y"].data.max() == 89.5
        assert xrimage.data.min() == 10
        assert xrimage.data.max() == 255
        assert xrimage.data.dtype == np.uint8

        if _HAS_RIOXARRAY:  # Full check if rioxarray is installed.
            xr.testing.assert_equal(xrimage, expected_xrimage)


def test_clib_read_data_image_two_steps(expected_xrimage):
    """
    Test the Session.read_data method for images in two steps, first reading the header
    and then the data.
    """
    infile = "@earth_day_01d"
    with Session() as lib:
        # Read the header first
        data_ptr = lib.read_data(infile, kind="image", mode="GMT_CONTAINER_ONLY")
        image = data_ptr.contents
        header = image.header.contents
        assert header.n_rows == 180
        assert header.n_columns == 360
        assert header.wesn[:] == [-180.0, 180.0, -90.0, 90.0]
        assert header.n_bands == 3  # Explicitly check n_bands
        assert not image.data  # The data is not read yet

        # Read the data
        lib.read_data(infile, kind="image", mode="GMT_DATA_ONLY", data=data_ptr)

        xrimage = image.to_dataarray()
        assert xrimage.shape == (3, 180, 360)
        assert xrimage.coords["x"].data.min() == -179.5
        assert xrimage.coords["x"].data.max() == 179.5
        assert xrimage.coords["y"].data.min() == -89.5
        assert xrimage.coords["y"].data.max() == 89.5
        assert xrimage.data.min() == 10
        assert xrimage.data.max() == 255
        assert xrimage.data.dtype == np.uint8

        if _HAS_RIOXARRAY:  # Full check if rioxarray is installed.
            xr.testing.assert_equal(xrimage, expected_xrimage)


def test_clib_read_data_fails():
    """
    Test that the Session.read_data method raises an exception if there are errors.
    """
    with Session() as lib:
        with pytest.raises(GMTCLibError):
            lib.read_data("not-exists.txt", kind="dataset")
