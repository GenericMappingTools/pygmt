"""
Tests for grdsample.
"""
from pathlib import Path

import pytest
import xarray as xr
from pygmt import grdsample, load_dataarray
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    Return the region settings for the grdsample tests.
    """
    return [-53, -47, -20, -15]


@pytest.fixture(scope="module", name="spacing")
def fixture_spacing():
    """
    Return the spacing settings for the grdsample tests.
    """
    return [2, 1]


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected grdsample grid result.
    """
    return xr.DataArray(
        data=[
            [460.84375, 482.78125, 891.09375],
            [680.46875, 519.09375, 764.9375],
            [867.75, 579.03125, 852.53125],
            [551.75, 666.6875, 958.21875],
            [411.3125, 518.4375, 931.28125],
        ],
        coords=dict(
            lon=[-52, -50, -48],
            lat=[-19.5, -18.5, -17.5, -16.5, -15.5],
        ),
        dims=["lat", "lon"],
    )


def test_grdsample_file_out(grid, expected_grid, region, spacing):
    """
    Test grdsample with an outgrid set and the spacing is changed.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdsample(
            grid=grid, outgrid=tmpfile.name, spacing=spacing, region=region
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdsample_dataarray_out(grid, expected_grid, region, spacing):
    """
    Test grdsample with no outgrid set and the spacing is changed.
    """
    result = grdsample(grid=grid, spacing=spacing, region=region)
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdsample_registration_changes(grid):
    """
    Test grdsample with no set outgrid and applying registration changes.
    """
    assert grid.gmt.registration == 1  # Pixel registration
    translated_grid = grdsample(grid=grid, translate=True)
    assert translated_grid.gmt.registration == 0  # Gridline registration
    registration_grid = grdsample(grid=translated_grid, registration="p")
    assert registration_grid.gmt.registration == 1  # Pixel registration
