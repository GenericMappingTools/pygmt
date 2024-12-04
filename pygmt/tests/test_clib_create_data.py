"""
Test the Session.create_data method.
"""

import pytest
from pygmt import clib
from pygmt.exceptions import GMTCLibError, GMTInvalidInput
from pygmt.tests.test_clib import mock


def test_create_data_dataset():
    """
    Run the function to make sure it doesn't fail badly.
    """
    with clib.Session() as lib:
        # Dataset from vectors
        data_vector = lib.create_data(
            family="GMT_IS_DATASET|GMT_VIA_VECTOR",
            geometry="GMT_IS_POINT",
            mode="GMT_CONTAINER_ONLY",
            dim=[10, 20, 0, 0],  # ncolumns, nrows, dtype, unused
        )
        # Dataset from matrices
        data_matrix = lib.create_data(
            family="GMT_IS_DATASET|GMT_VIA_MATRIX",
            geometry="GMT_IS_POINT",
            mode="GMT_CONTAINER_ONLY",
            dim=[10, 20, 1, 0],  # ncolumns, nrows, nlayer, dtype
        )
        assert data_vector != data_matrix


def test_create_data_grid_dim():
    """
    Create a grid ignoring range and inc.
    """
    with clib.Session() as lib:
        # Grids from matrices using dim
        lib.create_data(
            family="GMT_IS_GRID|GMT_VIA_MATRIX",
            geometry="GMT_IS_SURFACE",
            mode="GMT_CONTAINER_ONLY",
            dim=[10, 20, 1, 0],  # ncolumns, nrows, nlayer, dtype
        )


def test_create_data_grid_range():
    """
    Create a grid specifying range and inc instead of dim.
    """
    with clib.Session() as lib:
        # Grids from matrices using range and int
        lib.create_data(
            family="GMT_IS_GRID|GMT_VIA_MATRIX",
            geometry="GMT_IS_SURFACE",
            mode="GMT_CONTAINER_ONLY",
            ranges=[150.0, 250.0, -20.0, 20.0],
            inc=[0.1, 0.2],
        )


def test_create_data_fails():
    """
    Check that create_data raises exceptions for invalid input and output.
    """
    # Passing in invalid mode
    with pytest.raises(GMTInvalidInput):
        with clib.Session() as lib:
            lib.create_data(
                family="GMT_IS_DATASET",
                geometry="GMT_IS_SURFACE",
                mode="Not_a_valid_mode",
                dim=[0, 0, 1, 0],
                ranges=[150.0, 250.0, -20.0, 20.0],
                inc=[0.1, 0.2],
            )
    # Passing in invalid geometry
    with pytest.raises(GMTInvalidInput):
        with clib.Session() as lib:
            lib.create_data(
                family="GMT_IS_GRID",
                geometry="Not_a_valid_geometry",
                mode="GMT_CONTAINER_ONLY",
                dim=[0, 0, 1, 0],
                ranges=[150.0, 250.0, -20.0, 20.0],
                inc=[0.1, 0.2],
            )

    # If the data pointer returned is None (NULL pointer)
    with clib.Session() as lib:
        with mock(lib, "GMT_Create_Data", returns=None):
            with pytest.raises(GMTCLibError):
                lib.create_data(
                    family="GMT_IS_DATASET",
                    geometry="GMT_IS_SURFACE",
                    mode="GMT_CONTAINER_ONLY",
                    dim=[11, 10, 2, 0],  # n_tables, n_segments, n_rows, n_columns
                )
