"""
Tests for grdmath.
"""
import numpy as np
import pytest
import xarray as xr
import xarray.testing as xrt
from pygmt import GrdMathCalc
from pygmt.datasets import load_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[0, 3, 6, 9])


def test_grdmath_sqrt(grid):
    """
    Test grdmath SQRT operation.
    """
    grdcalc = GrdMathCalc()
    actual = grdcalc.sqrt(ingrid="@earth_relief_01d", outgrid=True, region=[0, 3, 6, 9])
    expected = np.sqrt(grid)
    xrt.assert_allclose(actual, expected)


def test_grdmath_directly(grid):
    """
    Test grdmath LOG operation directly using GrdMathCalc.grdmath classmethod.
    """
    actual = GrdMathCalc.grdmath(
        operator="LOG", ingrid="@earth_relief_01d", outgrid=True, region=[0, 3, 6, 9]
    )
    expected = np.log(grid)
    xrt.assert_allclose(actual, expected)


def test_grdmath_chained_operations():
    """
    Test grdmath chaining several intermediate computations together before
    producing final xarray.DataArray grid by calling `.compute()`.
    """
    grdcalc = GrdMathCalc()
    assert grdcalc.arg_str == ""

    grid1 = grdcalc.sqrt(ingrid="@earth_relief_01d_p")
    assert grid1.arg_str == "@earth_relief_01d_p SQRT"

    grid2 = grdcalc.std(ingrid="@earth_relief_01d_g")
    assert grid2.arg_str == "@earth_relief_01d_g STD"

    grid3 = grid1.multiply(ingrid=grid2, region=[0, 3, 6, 9])
    assert (
        grid3.arg_str == "@earth_relief_01d_p SQRT @earth_relief_01d_g STD "
        "-R0/3/6/9 MUL"
    )

    actual_grid = grid3.compute()
    expected_grid = xr.DataArray(
        data=[
            [5297.7134, 3454.636, 887.0686],
            [9147.278, 6667.7827, 5760.257],
            [8469.841, 8661.23, 7892.7505],
        ],
        coords=dict(lon=[0.5, 1.5, 2.5], lat=[6.5, 7.5, 8.5]),
        dims=["lat", "lon"],
    )
    xrt.assert_allclose(actual_grid, expected_grid)
