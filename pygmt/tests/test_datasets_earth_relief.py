"""
Test basic functionality for loading Earth relief datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput


@pytest.mark.parametrize("data_source", ["igpp", "gebco", "gebcosi", "synbath"])
def test_earth_relief_fails(data_source):
    """
    Make sure earth relief fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_relief(resolution=resolution, data_source=data_source)


# Only test 01d and 30m to avoid downloading large datasets in CI
@pytest.mark.parametrize("data_source", ["igpp", "synbath"])
def test_earth_relief_01d_igpp_synbath(data_source):
    """
    Test some properties of the earth relief 01d data with IGPP and SYNBATH
    data.
    """
    data = load_earth_relief(
        resolution="01d", registration="gridline", data_source=data_source
    )
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -8600.5)
    npt.assert_allclose(data.max(), 5559.0)


@pytest.mark.parametrize("data_source", ["gebco", "gebcosi"])
def test_earth_relief_01d_gebco(data_source):
    """
    Test some properties of the earth relief 01d data with GEBCO and GEBOCSI
    data.
    """
    data = load_earth_relief(
        resolution="01d", registration="gridline", data_source=data_source
    )
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -8598)
    npt.assert_allclose(data.max(), 5559.0)


def test_earth_relief_01d_with_region_srtm():
    """
    Test loading low-resolution earth relief with 'region' with IGPP data.
    """
    data = load_earth_relief(
        resolution="01d",
        region=[-10, 10, -5, 5],
        registration="gridline",
        data_source="igpp",
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -5154)
    npt.assert_allclose(data.max(), 805.5)


def test_earth_relief_01d_with_region_gebco():
    """
    Test loading low-resolution earth relief with 'region' with GEBCO data.
    """
    data = load_earth_relief(
        resolution="01d",
        region=[-10, 10, -5, 5],
        registration="gridline",
        data_source="gebco",
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -5146)
    npt.assert_allclose(data.max(), 806)


def test_earth_relief_30m():
    """
    Test some properties of the earth relief 30m data.
    """
    data = load_earth_relief(resolution="30m", registration="gridline")
    assert data.shape == (361, 721)
    npt.assert_allclose(data.lat, np.arange(-90, 90.5, 0.5))
    npt.assert_allclose(data.lon, np.arange(-180, 180.5, 0.5))
    npt.assert_allclose(data.min(), -9454.5)
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


def test_earth_gebcosi_15m_with_region():
    """
    Test loading a subregion of 15 arc-minute resolution earth_gebcosi grid.
    """
    data = load_earth_relief(
        resolution="15m",
        region=[85, 87, -88, -84],
        registration="pixel",
        data_source="gebcosi",
    )
    assert data.shape == (16, 8)
    npt.assert_allclose(data.lat, np.arange(-87.875, -84, 0.25))
    npt.assert_allclose(data.lon, np.arange(85.125, 87, 0.25))
    npt.assert_allclose(data.min(), -531)
    npt.assert_allclose(data.max(), 474)
    
    
def test_earth_relief_30s_synbath():
    """
    Test some properties of the earth relief 30s data with SYNBATH data.
    """
    data = load_earth_relief(
        region=[-95, -94, -1.5, -1],
        resolution="30s",
        registration="pixel",
        data_source="synbath",
    )
    assert data.shape == (60, 120)
    npt.assert_allclose(data.min(), -3552.5)
    npt.assert_allclose(data.max(), -2154)


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


def test_earth_relief_invalid_data_source():
    """
    Test loading earth relief with invalid data_source argument.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_relief(
            resolution="01d", registration="gridline", data_source="invalid_source"
        )


def test_earth_relief_invalid_data_source_with_use_srtm():
    """
    Test loading earth relief with use_srtm=True and an incompatible
    data_source argument.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_relief(
            resolution="03s",
            region=[135, 136, 35, 36],
            registration="gridline",
            use_srtm=True,
            data_source="gebco",
        )
