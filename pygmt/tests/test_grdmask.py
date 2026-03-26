"""
Test pygmt.grdmask.
"""

from pathlib import Path

import numpy as np
import pytest
import xarray as xr
from pygmt import grdmask
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="polygon_data")
def fixture_polygon_data():
    """
    Create a simple polygon for testing.
    A triangle polygon covering the region [125, 130, 30, 35].
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
    # Check that we have values in the expected range
    assert result.values.max() <= 30.0
    assert result.values.min() >= 0.0


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


def test_grdmask_invalid_combination(polygon_data):
    """
    Check that grdmask fails when inside and edge have different special modes.
    """
    with pytest.raises(GMTValueError):
        grdmask(
            data=polygon_data,
            spacing=1,
            region=[125, 130, 30, 35],
            inside="z",
            edge="id",
        )


@pytest.mark.parametrize(
    ("edge", "inside"),
    [("z", None), ("id", None), ("z", 5), ("id", 5)],
)
def test_grdmask_invalid_edge_special_mode(polygon_data, edge, inside):
    """
    Check that special edge modes require the same special inside mode.
    """
    with pytest.raises(GMTValueError):
        grdmask(
            data=polygon_data,
            spacing=1,
            region=[125, 130, 30, 35],
            edge=edge,
            inside=inside,
        )


@pytest.mark.parametrize(
    ("edge", "inside", "id_start"),
    [(None, "id", 5), ("id", "id", 10), (None, "id", -1), (None, "id", 1.5)],
)
def test_grdmask_id_start_valid(polygon_data, edge, inside, id_start):
    """
    Check that id_start works when inside='id'.
    """
    result = grdmask(
        data=polygon_data,
        spacing=1,
        region=[125, 130, 30, 35],
        edge=edge,
        inside=inside,
        id_start=id_start,
    )
    assert isinstance(result, xr.DataArray)
    unique_values = np.unique(result.values)
    assert id_start in unique_values
    assert 0 in unique_values


def test_grdmask_id_start_bool_invalid_value(polygon_data):
    """
    Check that bool id_start is rejected.
    """
    with pytest.raises(GMTValueError):
        grdmask(
            data=polygon_data,
            spacing=1,
            region=[125, 130, 30, 35],
            inside="id",
            id_start=True,
        )


def test_grdmask_id_start_requires_inside_id(polygon_data):
    """
    Check that id_start requires inside='id'.
    """
    with pytest.raises(GMTParameterError):
        grdmask(
            data=polygon_data,
            spacing=1,
            region=[125, 130, 30, 35],
            inside="z",
            id_start=5,
        )


def test_grdmask_id_start_requires_inside_id_when_inside_omitted(polygon_data):
    """
    Check that id_start requires inside='id' when inside is omitted.
    """
    with pytest.raises(GMTParameterError):
        grdmask(
            data=polygon_data,
            spacing=1,
            region=[125, 130, 30, 35],
            id_start=5,
        )


def test_grdmask_id_start_requires_inside_id_with_edge_and_outside(polygon_data):
    """
    Check that id_start still requires inside='id' even if edge and outside are set.
    """
    with pytest.raises(GMTParameterError):
        grdmask(
            data=polygon_data,
            spacing=1,
            region=[125, 130, 30, 35],
            outside=3,
            edge="id",
            id_start=5,
        )
