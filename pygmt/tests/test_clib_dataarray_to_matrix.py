"""
Test the dataarray_to_matrix function.
"""

import numpy as np
import numpy.testing as npt
import pytest
import xarray as xr
from pygmt.clib.conversion import dataarray_to_matrix
from pygmt.exceptions import GMTInvalidInput


@pytest.mark.benchmark
def test_dataarray_to_matrix_works():
    """
    Check that dataarray_to_matrix returns correct output.
    """
    data = np.diag(v=np.arange(3))
    x = np.linspace(start=0, stop=4, num=3)
    y = np.linspace(start=5, stop=9, num=3)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])

    matrix, region, inc = dataarray_to_matrix(grid)
    npt.assert_allclose(actual=matrix, desired=np.flipud(data))
    npt.assert_allclose(actual=region, desired=[x.min(), x.max(), y.min(), y.max()])
    npt.assert_allclose(actual=inc, desired=[x[1] - x[0], y[1] - y[0]])


def test_dataarray_to_matrix_negative_x_increment():
    """
    Check if dataarray_to_matrix returns correct output with flipped x.
    """
    data = np.diag(v=np.arange(3))
    x = np.linspace(start=4, stop=0, num=3)
    y = np.linspace(start=5, stop=9, num=3)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])

    matrix, region, inc = dataarray_to_matrix(grid)
    npt.assert_allclose(actual=matrix, desired=np.flip(data, axis=(0, 1)))
    npt.assert_allclose(actual=region, desired=[x.min(), x.max(), y.min(), y.max()])
    npt.assert_allclose(actual=inc, desired=[abs(x[1] - x[0]), abs(y[1] - y[0])])


def test_dataarray_to_matrix_negative_y_increment():
    """
    Check that dataarray_to_matrix returns correct output with flipped y.
    """
    data = np.diag(v=np.arange(3))
    x = np.linspace(start=0, stop=4, num=3)
    y = np.linspace(start=9, stop=5, num=3)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])

    matrix, region, inc = dataarray_to_matrix(grid)
    npt.assert_allclose(actual=matrix, desired=data)
    npt.assert_allclose(actual=region, desired=[x.min(), x.max(), y.min(), y.max()])
    npt.assert_allclose(actual=inc, desired=[abs(x[1] - x[0]), abs(y[1] - y[0])])


def test_dataarray_to_matrix_negative_x_and_y_increment():
    """
    Check that dataarray_to_matrix returns correct output with flipped x/y.
    """
    data = np.diag(v=np.arange(3))
    x = np.linspace(start=4, stop=0, num=3)
    y = np.linspace(start=9, stop=5, num=3)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])

    matrix, region, inc = dataarray_to_matrix(grid)
    npt.assert_allclose(actual=matrix, desired=np.fliplr(data))
    npt.assert_allclose(actual=region, desired=[x.min(), x.max(), y.min(), y.max()])
    npt.assert_allclose(actual=inc, desired=[abs(x[1] - x[0]), abs(y[1] - y[0])])


def test_dataarray_to_matrix_dims_fails():
    """
    Check that it fails for > 2 dims.
    """
    # Make a 3-D regular grid
    data = np.ones((10, 12, 11), dtype=np.float32)
    x = np.arange(11)
    y = np.arange(12)
    z = np.arange(10)
    grid = xr.DataArray(data, coords=[("z", z), ("y", y), ("x", x)])
    with pytest.raises(GMTInvalidInput):
        dataarray_to_matrix(grid)


def test_dataarray_to_matrix_irregular_inc_warning():
    """
    Check that it warns for variable increments, see also
    https://github.com/GenericMappingTools/pygmt/issues/1468.
    """
    data = np.ones((4, 5), dtype=np.float64)
    x = np.linspace(0, 1, 5)
    y = np.logspace(2, 3, 4)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])
    with pytest.warns(expected_warning=RuntimeWarning) as record:
        dataarray_to_matrix(grid)
        assert len(record) == 1


def test_dataarray_to_matrix_zero_inc_fails():
    """
    Check that dataarray_to_matrix fails for zero increments grid.
    """
    data = np.ones((5, 5), dtype=np.float32)
    x = np.linspace(0, 1, 5)
    y = np.zeros_like(x)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])
    with pytest.raises(GMTInvalidInput):
        dataarray_to_matrix(grid)

    y = np.linspace(0, 1, 5)
    x = np.zeros_like(x)
    grid = xr.DataArray(data, coords=[("y", y), ("x", x)])
    with pytest.raises(GMTInvalidInput):
        dataarray_to_matrix(grid)
