"""
Tests for xyz2grd.
"""
from pathlib import Path

import numpy as np
import pytest
import xarray as xr
from pygmt import load_dataarray, xyz2grd
from pygmt.datasets import load_sample_data
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="ship_data")
def fixture_ship_data():
    """
    Load the table data from the sample bathymetry dataset.
    """
    return load_sample_data(name="bathymetry")


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected xyz2grd grid result.
    """
    return xr.DataArray(
        data=[
            [-3651.0608, -3015.214, -2320.1033],
            [-2546.2512, -1977.8754, -963.23303],
            [-352.3795, -1025.4508, np.nan],
        ],
        coords=dict(
            x=[245.0, 250.0, 255.0],
            y=[20.0, 25.0, 30.0],
        ),
        dims=["y", "x"],
    )


@pytest.mark.parametrize("array_func", [np.array, xr.Dataset])
def test_xyz2grd_input_array(array_func, ship_data, expected_grid):
    """
    Run xyz2grd by passing in an xarray dataset or numpy array.
    """
    output = xyz2grd(data=array_func(ship_data), spacing=5, region=[245, 255, 20, 30])
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type
    xr.testing.assert_allclose(a=output, b=expected_grid)


def test_xyz2grd_input_array_file_out(ship_data, expected_grid):
    """
    Run xyz2grd by passing in a numpy array and set an outgrid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = xyz2grd(
            data=ship_data,
            spacing=5,
            region=[245, 255, 20, 30],
            outgrid=tmpfile.name,
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_xyz2grd_missing_region_spacing(ship_data):
    """
    Test xyz2grd raise an exception if region or spacing is missing.
    """
    with pytest.raises(GMTInvalidInput):
        xyz2grd(data=ship_data)
    with pytest.raises(GMTInvalidInput):
        xyz2grd(data=ship_data, region=[245, 255, 20, 30])
    with pytest.raises(GMTInvalidInput):
        xyz2grd(data=ship_data, spacing=5)
