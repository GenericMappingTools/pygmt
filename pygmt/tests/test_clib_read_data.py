"""
Test the Session.read_data method.
"""

from pathlib import Path

import pandas as pd
import pytest
import xarray as xr
from pygmt.clib import Session
from pygmt.helpers import GMTTempFile
from pygmt.io import load_dataarray
from pygmt.src import which


@pytest.fixture(scope="module", name="expected_xrgrid")
def fixture_expected_xrgrid():
    """
    The expected xr.DataArray object for the static_earth_relief.nc file.
    """
    return load_dataarray(which("@static_earth_relief.nc"))


def test_clib_read_data_dataset():
    """
    Test the Session.read_data method for datasets.

    The test is adapted from the doctest in the _GMT_DATASET class.
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

    The test is adapted from the doctest in the _GMT_GRID class.
    """
    with Session() as lib:
        grid = lib.read_data("@static_earth_relief.nc", kind="grid").contents
        xrgrid = grid.to_dataarray()
        xr.testing.assert_equal(xrgrid, expected_xrgrid)
        # Explicitely check n_bands
        assert grid.header.contents.n_bands == 1


def test_clib_read_data_grid_two_steps(expected_xrgrid):
    """
    Test the Session.read_data method for grids in two steps, first reading the header
    and then the data.

    The test is adapted from the doctest in the _GMT_GRID class.
    """
    infile = "@static_earth_relief.nc"
    with Session() as lib:
        # Read the header first
        data_ptr = lib.read_data(infile, kind="grid", mode="GMT_CONTAINER_ONLY")
        grid = data_ptr.contents
        header = grid.header.contents
        assert header.n_rows == 14
        assert header.n_columns == 8
        assert header.n_bands == 1
        assert header.wesn[:] == [-55.0, -47.0, -24.0, -10.0]
        assert header.z_min == 190.0
        assert header.z_max == 981.0

        assert not grid.data  # The data is not read yet

        # Read the data
        lib.read_data(infile, kind="grid", mode="GMT_DATA_ONLY", data=data_ptr)
        xrgrid = data_ptr.contents.to_dataarray()
        xr.testing.assert_equal(xrgrid, expected_xrgrid)
        # Explicitely check n_bands
        assert grid.header.contents.n_bands == 1


def test_clib_read_data_image_as_grid():
    """
    Test the Session.read_data method for images.
    """
    with Session() as lib:
        data_ptr = lib.read_data(
            "@earth_day_01d_p", kind="grid", mode="GMT_CONTAINER_AND_DATA"
        )
        image = data_ptr.contents
        header = image.header.contents
        assert header.n_rows == 180
        assert header.n_columns == 360
        assert header.n_bands == 1
        assert header.wesn[:] == [-180.0, 180.0, -90.0, 90.0]

        assert image.data
