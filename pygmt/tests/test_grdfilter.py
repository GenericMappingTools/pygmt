"""
Tests for grdfilter.
"""
import os

import numpy as np
import pytest
import xarray as xr
from pygmt import grdfilter, load_dataarray
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static earth relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected grdfilter grid result.
    """
    return xr.DataArray(
        data=[
            [
                349.32083,
                357.8113,
                410.9827,
                496.60913,
                552.44476,
                581.40717,
                611.51605,
                636.03265,
            ],
            [
                359.02524,
                353.88202,
                378.53894,
                434.549,
                490.8761,
                538.3713,
                586.06854,
                622.79504,
            ],
            [
                402.2158,
                381.7815,
                373.55005,
                393.34833,
                438.65378,
                499.6046,
                576.84,
                645.3407,
            ],
            [
                471.98853,
                443.75842,
                415.47766,
                410.1826,
                441.43887,
                512.685,
                617.2554,
                720.32916,
            ],
            [
                498.3717,
                504.52777,
                502.61914,
                488.27576,
                494.10657,
                559.06244,
                676.28284,
                786.73645,
            ],
            [
                491.36545,
                559.9697,
                614.6496,
                601.4992,
                569.9743,
                606.0966,
                705.7535,
                795.02405,
            ],
            [
                505.6051,
                592.4027,
                661.41003,
                656.9681,
                625.1668,
                664.40204,
                756.8206,
                827.8964,
            ],
            [
                500.1734,
                556.3298,
                583.0743,
                570.61896,
                588.92017,
                687.3645,
                803.91034,
                875.61707,
            ],
            [
                509.3999,
                508.7543,
                473.5177,
                430.1827,
                473.86908,
                614.1568,
                765.8883,
                866.7539,
            ],
            [
                483.52835,
                453.9541,
                391.97992,
                333.6773,
                365.24432,
                497.22,
                660.1798,
                786.3931,
            ],
            [
                420.85852,
                394.6937,
                345.36194,
                292.87177,
                296.38342,
                384.7768,
                518.4832,
                628.54156,
            ],
            [
                363.77417,
                348.02396,
                319.9753,
                275.95178,
                253.69693,
                292.9342,
                375.33408,
                446.69897,
            ],
            [
                340.42834,
                328.41458,
                306.3464,
                264.70032,
                230.80988,
                247.023,
                305.89627,
                364.31616,
            ],
            [
                338.35388,
                326.14734,
                303.5548,
                262.39865,
                224.76819,
                235.73428,
                289.62326,
                341.76697,
            ],
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


def test_grdfilter_dataarray_in_dataarray_out(grid, expected_grid):
    """
    Test grdfilter with an input DataArray, and output as DataArray.
    """
    result = grdfilter(grid=grid, filter="g600", distance="4")
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdfilter_dataarray_in_file_out(grid, expected_grid):
    """
    Test grdfilter with an input DataArray, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdfilter(grid, outgrid=tmpfile.name, filter="g600", distance="4")
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdfilter_fails():
    """
    Check that grdfilter fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdfilter(np.arange(10).reshape((5, 2)))
