"""
Test the functions that put matrix data into GMT.
"""
import numpy as np
import numpy.testing as npt
import pytest
import xarray as xr
from pygmt import clib
from pygmt.exceptions import GMTCLibError
from pygmt.helpers import GMTTempFile
from pygmt.tests.test_clib import mock


@pytest.fixture(scope="module", name="dtypes")
def fixture_dtypes():
    """
    List of supported numpy dtypes.
    """
    return "int8 int16 int32 int64 uint8 uint16 uint32 uint64 float32 float64".split()


def test_put_matrix(dtypes):
    """
    Check that assigning a numpy 2-D array to a dataset works.
    """
    shape = (3, 4)
    for dtype in dtypes:
        with clib.Session() as lib:
            dataset = lib.create_data(
                family="GMT_IS_DATASET|GMT_VIA_MATRIX",
                geometry="GMT_IS_POINT",
                mode="GMT_CONTAINER_ONLY",
                dim=[shape[1], shape[0], 1, 0],  # columns, rows, layers, dtype
            )
            data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
            lib.put_matrix(dataset, matrix=data)
            # wesn doesn't matter for Datasets
            wesn = [0] * 6
            # Save the data to a file to see if it's being accessed correctly
            with GMTTempFile() as tmp_file:
                lib.write_data(
                    "GMT_IS_MATRIX",
                    "GMT_IS_POINT",
                    "GMT_WRITE_SET",
                    wesn,
                    tmp_file.name,
                    dataset,
                )
                # Load the data and check that it's correct
                newdata = tmp_file.loadtxt(dtype=dtype)
                npt.assert_allclose(newdata, data)


def test_put_matrix_fails():
    """
    Check that put_matrix raises an exception if return code is not zero.
    """
    # It's hard to make put_matrix fail on the C API level because of all the
    # checks on input arguments. Mock the C API function just to make sure it
    # works.
    with clib.Session() as lib:
        with mock(lib, "GMT_Put_Matrix", returns=1):
            with pytest.raises(GMTCLibError):
                lib.put_matrix(dataset=None, matrix=np.empty((10, 2)), pad=0)


def test_put_matrix_grid(dtypes):
    """
    Check that assigning a numpy 2-D array to an ASCII and netCDF grid works.
    """
    wesn = [10, 15, 30, 40, 0, 0]
    inc = [1, 1]
    shape = ((wesn[3] - wesn[2]) // inc[1] + 1, (wesn[1] - wesn[0]) // inc[0] + 1)
    for dtype in dtypes:
        with clib.Session() as lib:
            grid = lib.create_data(
                family="GMT_IS_GRID|GMT_VIA_MATRIX",
                geometry="GMT_IS_SURFACE",
                mode="GMT_CONTAINER_ONLY",
                ranges=wesn[:4],
                inc=inc,
                registration="GMT_GRID_NODE_REG",
            )
            data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
            lib.put_matrix(grid, matrix=data)
            # Save the data to a file to see if it's being accessed correctly
            with GMTTempFile() as tmp_file:
                lib.write_data(
                    "GMT_IS_MATRIX",
                    "GMT_IS_POINT",
                    "GMT_CONTAINER_AND_DATA",
                    wesn,
                    tmp_file.name,
                    grid,
                )
                # Load the data and check that it's correct
                newdata = tmp_file.loadtxt(dtype=dtype)
                npt.assert_allclose(newdata, data)

            # Save the data to a netCDF grid and check that xarray can load it
            with GMTTempFile(suffix=".nc") as tmp_grid:
                lib.write_data(
                    "GMT_IS_MATRIX",
                    "GMT_IS_SURFACE",
                    "GMT_CONTAINER_AND_DATA",
                    wesn,
                    tmp_grid.name,
                    grid,
                )
                with xr.open_dataarray(tmp_grid.name) as dataarray:
                    assert dataarray.shape == shape
                    npt.assert_allclose(dataarray.data, np.flipud(data))
                    npt.assert_allclose(
                        dataarray.coords["x"].actual_range, np.array(wesn[0:2])
                    )
                    npt.assert_allclose(
                        dataarray.coords["y"].actual_range, np.array(wesn[2:4])
                    )
