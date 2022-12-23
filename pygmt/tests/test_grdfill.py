"""
Tests for grdfill.
"""
from pathlib import Path

import numpy as np
import pytest
import xarray as xr
from packaging.version import Version
from pygmt import clib, grdfill, load_dataarray
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief

with clib.Session() as _lib:
    gmt_version = Version(_lib.info["version"])


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file and set value(s) to
    NaN and inf.
    """
    grid = load_static_earth_relief()
    grid[3:6, 3:5] = np.nan
    grid[6:8, 2:4] = np.inf
    return grid


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected grdfill grid result.
    """
    return xr.DataArray(
        data=[
            [347.5, 344.5, 386.0, 640.5, 617.0, 579.0, 646.5, 671.0],
            [383.0, 284.5, 344.5, 394.0, 491.0, 556.5, 578.5, 618.5],
            [373.0, 367.5, 349.0, 352.5, 419.5, 428.0, 570.0, 667.5],
            [557.0, 435.0, 385.5, 20.0, 20.0, 496.0, 519.5, 833.5],
            [561.5, 539.0, 446.5, 20.0, 20.0, 553.0, 726.5, 981.0],
            [310.0, 521.5, 757.0, 20.0, 20.0, 524.0, 686.5, 794.0],
            [521.5, 682.5, np.inf, np.inf, 571.5, 638.5, 739.5, 881.5],
            [308.0, 595.5, np.inf, np.inf, 580.0, 770.0, 927.0, 920.0],
            [601.0, 526.5, 535.0, 299.0, 398.5, 645.0, 797.5, 964.0],
            [494.5, 488.5, 357.0, 254.5, 286.0, 484.5, 653.5, 930.0],
            [450.5, 395.5, 366.0, 248.0, 250.0, 354.5, 550.0, 797.5],
            [345.5, 320.0, 335.0, 292.0, 207.5, 247.0, 325.0, 346.5],
            [349.0, 313.0, 325.5, 247.0, 191.0, 225.0, 260.0, 452.5],
            [347.5, 331.5, 309.0, 282.0, 190.0, 208.0, 299.5, 348.0],
        ],
        coords=dict(
            lon=[-54.5, -53.5, -52.5, -51.5, -50.5, -49.5, -48.5, -47.5],
            lat=[
                -23.5,
                -22.5,
                -21.5,
                -20.5,
                -19.5,
                -18.5,
                -17.5,
                -16.5,
                -15.5,
                -14.5,
                -13.5,
                -12.5,
                -11.5,
                -10.5,
            ],
        ),
        dims=["lat", "lon"],
    )


def test_grdfill_dataarray_out(grid, expected_grid):
    """
    Test grdfill with a DataArray output.
    """
    result = grdfill(grid=grid, mode="c20")
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


@pytest.mark.skipif(
    gmt_version < Version("6.4.0"),
    reason="Upstream bug/crash fixed in https://github.com/GenericMappingTools/gmt/pull/6418.",
)
def test_grdfill_asymmetric_pad(grid, expected_grid):
    """
    Test grdfill using a region that includes the edge of the grid.

    Regression test for
    https://github.com/GenericMappingTools/pygmt/issues/1745.
    """
    result = grdfill(grid=grid, mode="c20", region=[-55, -50, -24, -16])
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(
        a=result, b=expected_grid.sel(lon=slice(-55, -50), lat=slice(-24, -16))
    )


def test_grdfill_file_out(grid, expected_grid):
    """
    Test grdfill with an outgrid set.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdfill(grid=grid, mode="c20", outgrid=tmpfile.name)
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outfile exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdfill_required_args(grid):
    """
    Test that grdfill fails without arguments for `mode` and `L`.
    """
    with pytest.raises(GMTInvalidInput):
        grdfill(grid=grid)
