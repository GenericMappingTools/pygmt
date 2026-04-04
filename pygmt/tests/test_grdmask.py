"""
Test pygmt.grdmask.
"""

from pathlib import Path

import numpy as np
import pytest
import xarray as xr
from pygmt import grdmask
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="polygon_data")
def fixture_polygon_data():
    """
    Create a simple polygon for testing.
    """
    return np.array([[125, 30], [130, 30], [130, 35], [125, 30]])


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected grdmask grid result.
    """
    return xr.DataArray(
        data=[
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 1.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
        coords={
            "x": [125.0, 126.0, 127.0, 128.0, 129.0, 130.0],
            "y": [30.0, 31.0, 32.0, 33.0, 34.0, 35.0],
        },
        dims=["y", "x"],
    )


@pytest.fixture(scope="module", name="expected_grid_outside_only")
def fixture_expected_grid_outside_only():
    """
    Load the expected grdmask grid result when only outside is set.
    """
    return xr.DataArray(
        data=[
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [3.0, 0.0, 1.0, 1.0, 1.0, 0.0],
            [3.0, 3.0, 0.0, 1.0, 1.0, 0.0],
            [3.0, 3.0, 3.0, 0.0, 1.0, 0.0],
            [3.0, 3.0, 3.0, 3.0, 0.0, 0.0],
            [3.0, 3.0, 3.0, 3.0, 3.0, 0.0],
        ],
        coords={
            "x": [125.0, 126.0, 127.0, 128.0, 129.0, 130.0],
            "y": [30.0, 31.0, 32.0, 33.0, 34.0, 35.0],
        },
        dims=["y", "x"],
    )


def test_grdmask_outgrid(polygon_data, expected_grid):
    """
    Creates a mask grid with an outgrid argument.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdmask(
            data=polygon_data,
            outgrid=tmpfile.name,
            spacing=1,
            region=[125, 130, 30, 35],
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
        temp_grid = xr.load_dataarray(tmpfile.name, engine="gmt", raster_kind="grid")
        # Check grid properties
        assert temp_grid.dims == ("y", "x")
        assert temp_grid.gmt.gtype is GridType.CARTESIAN
        assert temp_grid.gmt.registration is GridRegistration.GRIDLINE
        # Check grid values
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


@pytest.mark.benchmark
def test_grdmask_no_outgrid(polygon_data, expected_grid):
    """
    Test grdmask with no set outgrid.
    """
    result = grdmask(data=polygon_data, spacing=1, region=[125, 130, 30, 35])
    # Check grid properties
    assert isinstance(result, xr.DataArray)
    assert result.dims == ("y", "x")
    assert result.gmt.gtype is GridType.CARTESIAN
    assert result.gmt.registration is GridRegistration.GRIDLINE
    # Check grid values
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdmask_custom_mask_values(polygon_data):
    """
    Test grdmask with custom outside, edge, inside values.
    """
    result = grdmask(
        data=polygon_data,
        spacing=1,
        region=[125, 130, 30, 35],
        outside=10,
        edge=20,
        inside=30,
    )
    assert isinstance(result, xr.DataArray)
    # Check that the grid has the right dimensions
    assert result.shape == (6, 6)
    # Check that we have expected values
    assert result.sel(x=125, y=35) == 10.0  # outside
    assert result.sel(x=128, y=30) == 20.0  # edge
    assert result.sel(x=129, y=31) == 30.0  # inside


def test_grdmask_outside_only(polygon_data, expected_grid_outside_only):
    """
    Test grdmask when only outside is set.
    """
    result = grdmask(
        data=polygon_data,
        spacing=1,
        region=[125, 130, 30, 35],
        outside=3,
    )

    assert isinstance(result, xr.DataArray)
    assert result.dims == ("y", "x")
    assert result.gmt.gtype is GridType.CARTESIAN
    assert result.gmt.registration is GridRegistration.GRIDLINE
    xr.testing.assert_allclose(a=result, b=expected_grid_outside_only)


def test_grdmask_fails():
    """
    Check that grdmask fails correctly when region and spacing are not given.
    """
    with pytest.raises(GMTParameterError):
        grdmask(data=np.array([[0, 0], [1, 1], [1, 0], [0, 0]]))


@pytest.mark.parametrize(
    ("edge", "id_start"),
    [(None, 5), ("id", 10), (None, -1), (None, 1.5)],
)
def test_grdmask_id_start_valid(polygon_data, edge, id_start):
    """
    Check that id_start works when inside='id'.
    """
    result = grdmask(
        data=polygon_data,
        spacing=1,
        region=[125, 130, 30, 35],
        edge=edge,
        inside="id",
        id_start=id_start,
    )
    assert isinstance(result, xr.DataArray)
    unique_values = np.unique(result.values)
    assert id_start in unique_values
