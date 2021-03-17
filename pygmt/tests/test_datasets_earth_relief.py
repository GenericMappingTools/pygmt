"""
Test basic functionality for loading Earth relief datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput


def test_earth_relief_fails():
    """
    Make sure earth relief fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_relief(resolution=resolution)


# Only test 01d and 30m to avoid downloading large datasets in CI
def test_earth_relief_01d():
    """
    Test some properties of the earth relief 01d data.
    """
    data = load_earth_relief(resolution="01d", registration="gridline")
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -8592.5)
    npt.assert_allclose(data.max(), 5559.0)


def test_earth_relief_01d_with_region():
    """
    Test loading low-resolution earth relief with 'region'.
    """
    data = load_earth_relief(
        resolution="01d", region=[-10, 10, -5, 5], registration="gridline"
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -5145)
    npt.assert_allclose(data.max(), 805.5)


def test_earth_relief_30m():
    """
    Test some properties of the earth relief 30m data.
    """
    data = load_earth_relief(resolution="30m", registration="gridline")
    assert data.shape == (361, 721)
    npt.assert_allclose(data.lat, np.arange(-90, 90.5, 0.5))
    npt.assert_allclose(data.lon, np.arange(-180, 180.5, 0.5))
    npt.assert_allclose(data.min(), -9460.5)
    npt.assert_allclose(data.max(), 5887.5)


def test_earth_relief_05m_with_region():
    """
    Test loading a subregion of high-resolution earth relief grid.
    """
    data = load_earth_relief(
        resolution="05m", region=[120, 160, 30, 60], registration="gridline"
    )
    assert data.coords["lat"].data.min() == 30.0
    assert data.coords["lat"].data.max() == 60.0
    assert data.coords["lon"].data.min() == 120.0
    assert data.coords["lon"].data.max() == 160.0
    assert data.data.min() == -9633.0
    assert data.data.max() == 2532.0
    assert data.sizes["lat"] == 361
    assert data.sizes["lon"] == 481


def test_earth_relief_05m_without_region():
    """
    Test loading high-resolution earth relief without passing 'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_relief("05m")


def test_earth_relief_03s_landonly_srtm():
    """
    Test loading original 3 arc-second land-only SRTM tiles.
    """
    data = load_earth_relief(
        "03s", region=[135, 136, 35, 36], registration="gridline", use_srtm=True
    )

    assert data.coords["lat"].data.min() == 35.0
    assert data.coords["lat"].data.max() == 36.0
    assert data.coords["lon"].data.min() == 135.0
    assert data.coords["lon"].data.max() == 136.0
    # data.data.min() == -305.51846 if use_srtm is False.
    assert data.data.min() == -6.0
    assert data.data.max() == 1191.0
    assert data.sizes["lat"] == 1201
    assert data.sizes["lon"] == 1201


def test_earth_relief_incorrect_registration():
    """
    Test loading earth relief with incorrect registration type.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_relief(registration="improper_type")


def test_earth_relief_invalid_resolution_registration_combination():
    """
    Test loading earth relief with invalid combination of resolution and
    registration.
    """
    for resolution, registration in [
        ("15s", "gridline"),
        ("03s", "pixel"),
        ("01s", "pixel"),
    ]:
        with pytest.raises(GMTInvalidInput):
            load_earth_relief(resolution=resolution, registration=registration)
