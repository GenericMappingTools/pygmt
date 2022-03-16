"""
Tests for earthtide.
"""
import os

import pytest
import xarray as xr
from pygmt import earthtide, load_dataarray
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected earthtide grid result.
    """
    return xr.DataArray(
        data=[
            [0.04949933, 0.05444588, 0.05942686, 0.06443665],
            [0.05169343, 0.05663284, 0.06160447, 0.06660277],
            [0.05337802, 0.05829764, 0.06324723, 0.06822133],
        ],
        coords=dict(
            lon=[6.0, 7.0, 8.0, 9.0],
            lat=[13.0, 15.0, 17.0],
        ),
        dims=["lat", "lon"],
    )


def test_earthtide_outgrid(expected_grid):
    """
    Creates an earthtide grid with an outgrid argument.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = earthtide(
            outgrid=tmpfile.name,
            time="2018-06-18T12:00:00",
            region=[6, 9, 13, 17],
            spacing=[1, 2],
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_earthtide_no_outgrid(expected_grid):
    """
    Test earthtide with no set outgrid.
    """
    result = earthtide(
        time="2018-06-18T12:00:00", region=[6, 9, 13, 17], spacing=[1, 2]
    )
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 0  # Gridline registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_earthtide_fails():
    """
    Check that grdlandmask fails correctly when region is set but spacing is
    not.
    """
    with pytest.raises(GMTInvalidInput):
        earthtide(time="2018-06-18T12:00:00", region=[6, 9, 13, 17])
