"""
Tests for grdgradient.
"""
import os

import pytest
import xarray as xr
from pygmt import grdgradient, load_dataarray
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
    Load the expected grdgradient grid result.
    """
    return xr.DataArray(
        data=[
            [
                0.0003093,
                -0.00030156,
                0.00082771,
                -0.00321753,
                -0.0012325,
                0.00029303,
                -0.00071433,
                -0.00042325,
            ],
            [
                -9.2030154e-05,
                6.9311958e-05,
                -7.1301583e-05,
                -1.1515312e-03,
                -7.3724851e-04,
                -5.9472013e-04,
                -2.8636417e-04,
                -3.3669974e-05,
            ],
            [
                9.2409999e-04,
                6.4631621e-04,
                1.6897154e-04,
                -1.5560689e-04,
                -2.7983118e-04,
                -1.4160860e-04,
                -6.0275404e-05,
                1.0175415e-03,
            ],
            [
                0.0004817,
                0.00061649,
                0.00035715,
                0.00059459,
                0.00021403,
                0.0006419,
                0.00097437,
                0.0019272,
            ],
            [
                -0.00134312,
                0.00028779,
                0.00159748,
                0.00099057,
                0.00061276,
                0.00036173,
                0.00109405,
                0.00052379,
            ],
            [
                0.00055238,
                0.00100351,
                0.00158803,
                0.00161134,
                0.00054625,
                0.00050048,
                0.00027988,
                -0.00048961,
            ],
            [
                -9.3184717e-05,
                5.5243197e-04,
                -7.2569086e-04,
                -2.4801277e-04,
                -1.8859128e-05,
                1.2269041e-03,
                1.2639525e-03,
                8.3059818e-04,
            ],
            [
                0.00123278,
                -0.00048926,
                -0.00118795,
                -0.00257945,
                -0.00059182,
                0.00031137,
                0.000379,
                0.00034945,
            ],
            [
                0.00038143,
                -0.00052731,
                -0.00106336,
                -0.00144573,
                -0.00102155,
                -0.00094097,
                -0.00095265,
                0.00037731,
            ],
            [
                -0.00062573,
                -0.000691,
                -0.00093711,
                -0.00028311,
                -0.0004721,
                -0.00099002,
                -0.0007367,
                -0.00021186,
            ],
            [
                -7.9713057e-04,
                -8.1402151e-04,
                -2.1586697e-04,
                7.2911200e-05,
                -2.6209970e-04,
                -8.1081450e-04,
                -1.0989577e-03,
                -1.9306547e-03,
            ],
            [
                -0.00040348,
                -0.00037373,
                -0.00020174,
                -0.0001064,
                -0.00029726,
                -0.00047949,
                -0.00120463,
                -0.00193885,
            ],
            [
                -5.2498821e-05,
                3.2199980e-05,
                -1.6772587e-04,
                -1.5145564e-04,
                -9.5025178e-05,
                -1.1772248e-04,
                6.8355934e-05,
                4.8115075e-04,
            ],
            [
                -3.8696857e-05,
                1.6205679e-04,
                -1.6551542e-04,
                5.0331827e-04,
                -5.5473362e-04,
                -3.8908448e-04,
                6.5142877e-04,
                -8.4848242e-04,
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


def test_grdgradient_outgrid(grid, expected_grid):
    """
    Test the azimuth and direction parameters for grdgradient with a set
    outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdgradient(grid=grid, outgrid=tmpfile.name, azimuth=10, direction="c")
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdgradient_no_outgrid(grid, expected_grid):
    """
    Test the azimuth and direction parameters for grdgradient with no set
    outgrid.
    """
    result = grdgradient(grid=grid, azimuth=10, direction="c")
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdgradient_fails(grid):
    """
    Check that grdgradient fails correctly.

    Check that grdgradient fails correctly when `tiles` is specified but
    normalize is not.
    """
    with pytest.raises(GMTInvalidInput):
        grdgradient(grid=grid)  # fails without required arguments
    with pytest.raises(GMTInvalidInput):
        # fails when tiles is specified but not normalize
        grdgradient(grid=grid, azimuth=10, direction="c", tiles="c")
