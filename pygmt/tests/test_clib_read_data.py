"""
Test the Session.read_data method.
"""

import ctypes as ctp
from pathlib import Path

import numpy as np
from pygmt.clib import Session
from pygmt.datatypes import _GMT_DATASET, _GMT_GRID
from pygmt.helpers import GMTTempFile


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
            data_ptr = lib.read_data(
                "GMT_IS_DATASET",
                "GMT_IS_PLP",
                "GMT_READ_NORMAL",
                None,
                tmpfile.name,
                None,
            )
            ds = ctp.cast(data_ptr, ctp.POINTER(_GMT_DATASET)).contents

            assert ds.n_tables == 1
            assert ds.n_segments == 2
            assert ds.n_columns == 3

            tbl = ds.table[0].contents
            assert tbl.min[: tbl.n_columns] == [1.0, 2.0, 3.0]
            assert tbl.max[: tbl.n_columns] == [10.0, 11.0, 12.0]


def test_clib_read_data_grid():
    """
    Test the Session.read_data method for grids.

    The test is adapted from the doctest in the _GMT_GRID class.
    """
    with Session() as lib:
        data_ptr = lib.read_data(
            "GMT_IS_GRID",
            "GMT_IS_SURFACE",
            "GMT_CONTAINER_AND_DATA",
            None,
            "@static_earth_relief.nc",
            None,
        )
        grid = ctp.cast(data_ptr, ctp.POINTER(_GMT_GRID)).contents
        header = grid.header.contents
        assert header.n_rows == 14
        assert header.n_columns == 8
        assert header.n_bands == 1
        assert header.wesn[:] == [-55.0, -47.0, -24.0, -10.0]
        assert header.z_min == 190.0
        assert header.z_max == 981.0

        assert grid.data  # The data is read
        data = np.reshape(grid.data[: header.mx * header.my], (header.my, header.mx))
        data = data[
            header.pad[2] : header.my - header.pad[3],
            header.pad[0] : header.mx - header.pad[1],
        ]
        assert data[3][4] == 250.0


def test_clib_read_data_grid_two_steps():
    """
    Test the Session.read_data method for grids in two steps, first reading the header
    and then the data.

    The test is adapted from the doctest in the _GMT_GRID class.
    """
    family, geometry = "GMT_IS_GRID", "GMT_IS_SURFACE"
    infile = "@static_earth_relief.nc"
    with Session() as lib:
        # Read the header first
        data_ptr = lib.read_data(
            family, geometry, "GMT_CONTAINER_ONLY", None, infile, None
        )
        grid = ctp.cast(data_ptr, ctp.POINTER(_GMT_GRID)).contents
        header = grid.header.contents
        assert header.n_rows == 14
        assert header.n_columns == 8
        assert header.n_bands == 1
        assert header.wesn[:] == [-55.0, -47.0, -24.0, -10.0]
        assert header.z_min == 190.0
        assert header.z_max == 981.0

        assert not grid.data  # The data is not read yet

        # Read the data
        data_ptr = lib.read_data(
            family, geometry, "GMT_DATA_ONLY", None, infile, data_ptr
        )
        grid = ctp.cast(data_ptr, ctp.POINTER(_GMT_GRID)).contents

        assert grid.data  # The data is read
        header = grid.header.contents
        data = np.reshape(grid.data[: header.mx * header.my], (header.my, header.mx))
        data = data[
            header.pad[2] : header.my - header.pad[3],
            header.pad[0] : header.mx - header.pad[1],
        ]
        assert data[3][4] == 250.0


def test_clib_read_data_image_as_grid():
    """
    Test the Session.read_data method for images.
    """
    with Session() as lib:
        data_ptr = lib.read_data(
            "GMT_IS_GRID",
            "GMT_IS_SURFACE",
            "GMT_CONTAINER_AND_DATA",
            None,
            "@earth_day_01d_p",
            None,
        )
        image = ctp.cast(data_ptr, ctp.POINTER(_GMT_GRID)).contents
        header = image.header.contents
        assert header.n_rows == 180
        assert header.n_columns == 360
        assert header.n_bands == 1
        assert header.wesn[:] == [-180.0, 180.0, -90.0, 90.0]

        assert image.data
