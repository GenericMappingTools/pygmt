"""
Tests for grdproject.
"""
import os

import pytest
import xarray as xr
from pygmt import grdproject, load_dataarray
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected grdproject grid result.
    """
    return xr.DataArray(
        data=[
            [
                346.79022,
                345.2086,
                384.8157,
                648.1588,
                619.7381,
                578.44885,
                648.2733,
                672.07666,
            ],
            [
                382.15515,
                284.35507,
                345.97623,
                402.2099,
                496.62848,
                560.5301,
                580.74084,
                618.9018,
            ],
            [
                367.15283,
                360.61612,
                347.3465,
                354.10706,
                423.0196,
                432.20868,
                572.001,
                658.93726,
            ],
            [
                544.1669,
                426.3987,
                380.4458,
                340.0226,
                412.45425,
                488.2944,
                514.16327,
                816.1486,
            ],
            [
                574.0841,
                531.8546,
                427.2877,
                466.3097,
                432.7317,
                550.1912,
                711.32874,
                978.90344,
            ],
            [
                321.8456,
                515.88104,
                728.07733,
                548.088,
                528.31323,
                521.3422,
                688.95294,
                807.3097,
            ],
            [
                510.96704,
                672.04,
                806.90704,
                874.45685,
                568.82904,
                621.23413,
                724.951,
                870.13934,
            ],
            [
                314.1325,
                607.8976,
                578.2893,
                600.5781,
                588.48413,
                765.3087,
                917.0689,
                915.03644,
            ],
            [
                580.31305,
                533.4476,
                543.54504,
                320.22614,
                418.9647,
                663.88275,
                816.3481,
                962.22284,
            ],
            [
                505.7873,
                494.9686,
                369.4394,
                256.61102,
                294.76697,
                501.19598,
                667.80756,
                938.53253,
            ],
            [
                456.72577,
                403.76608,
                365.9512,
                246.51361,
                253.32127,
                365.70245,
                564.2224,
                822.5811,
            ],
            [
                349.83923,
                323.2676,
                336.66028,
                291.47055,
                209.76779,
                252.03117,
                336.52255,
                362.45535,
            ],
            [
                348.83423,
                312.71915,
                326.0617,
                247.48505,
                191.4082,
                225.82086,
                260.64087,
                451.4686,
            ],
            [
                347.52496,
                331.1457,
                309.23315,
                280.91202,
                190.87741,
                208.8518,
                298.5085,
                349.72183,
            ],
        ],
        coords=dict(
            x=[0.625, 1.875, 3.125, 4.375, 5.625, 6.875, 8.125, 9.375],
            y=[
                0.651503,
                1.954509,
                3.257516,
                4.560522,
                5.863528,
                7.166534,
                8.46954,
                9.772547,
                11.075553,
                12.378559,
                13.681565,
                14.984572,
                16.287578,
                17.590584,
            ],
        ),
        dims=["y", "x"],
    )


def test_grdproject_file_out(grid, expected_grid):
    """
    grdproject with an outgrid set.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdproject(grid=grid, projection="M10c", outgrid=tmpfile.name)
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        print(temp_grid)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdproject_no_outgrid(grid, expected_grid):
    """
    Test grdproject with no set outgrid.
    """
    assert grid.gmt.gtype == 1  # Geographic grid
    result = grdproject(grid=grid, projection="M10c")
    assert result.gmt.gtype == 0  # Rectangular grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdproject_fails(grid):
    """
    Check that grdproject fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdproject(grid=grid)
