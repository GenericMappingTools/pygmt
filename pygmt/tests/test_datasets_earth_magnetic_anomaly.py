"""
Test basic functionality for loading Earth magnetic anomaly datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_earth_magnetic_anomaly
from pygmt.exceptions import GMTInvalidInput


def test_earth_mag_fails():
    """
    Make sure earth_magnetic_anomaly fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_magnetic_anomaly(resolution=resolution)


def test_earth_mag_incorrect_registration():
    """
    Test loading earth_magnetic_anomaly with incorrect registration type.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_magnetic_anomaly(registration="improper_type")


def test_earth_mag_01d():
    """
    Test some properties of the magnetic anomaly 01d data.
    """
    data = load_earth_magnetic_anomaly(resolution="01d")
    assert data.name == "magnetic_anomaly"
    assert data.attrs["long_name"] == "Earth magnetic anomaly"
    assert data.attrs["units"] == "nT"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -384)
    npt.assert_allclose(data.max(), 1057.2)


def test_earth_mag_01d_with_region():
    """
    Test loading low-resolution earth magnetic anomaly with 'region'.
    """
    data = load_earth_magnetic_anomaly(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -180.40002)
    npt.assert_allclose(data.max(), 127.39996)


def test_earth_mag_02m_without_region():
    """
    Test loading high-resolution earth magnetic anomaly without passing
    'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_magnetic_anomaly("02m")


def test_earth_mag_incorrect_resolution_registration():
    """
    Test that an error is raised when trying to load a EMAG2 grid registration
    with an unavailable resolution.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_magnetic_anomaly(
            resolution="02m",
            region=[0, 1, 3, 5],
            registration="gridline",
            data_source="emag2_4km",
        )


def test_earth_mag4km_01d():
    """
    Test some properties of the magnetic anomaly 4km 01d data.
    """
    data = load_earth_magnetic_anomaly(resolution="01d", data_source="emag2_4km")
    assert data.name == "magnetic_anomaly"
    assert data.attrs["long_name"] == "Earth magnetic anomaly"
    assert data.attrs["units"] == "nT"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -799.19995)
    npt.assert_allclose(data.max(), 3226.4)


def test_earth_mag4km_01d_with_region():
    """
    Test loading low-resolution earth magnetic anomaly 4km 01d with 'region'.
    """
    data = load_earth_magnetic_anomaly(
        resolution="01d",
        region=[-10, 10, -5, 5],
        registration="gridline",
        data_source="emag2_4km",
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -153.19995)
    npt.assert_allclose(data.max(), 113.59985)


def test_earth_mag_02m_default_registration():
    """
    Test that the grid returned by default for the 2 arc-minute resolution has
    a "pixel" registration.
    """
    data = load_earth_magnetic_anomaly(resolution="02m", region=[-10, -9, 3, 5])
    assert data.shape == (60, 30)
    assert data.gmt.registration == 1
    npt.assert_allclose(data.coords["lat"].data.min(), 3.016666667)
    npt.assert_allclose(data.coords["lat"].data.max(), 4.983333333)
    npt.assert_allclose(data.coords["lon"].data.min(), -9.98333333)
    npt.assert_allclose(data.coords["lon"].data.max(), -9.01666667)
    npt.assert_allclose(data.min(), -231)
    npt.assert_allclose(data.max(), 131.79999)

    data = load_earth_magnetic_anomaly(
        resolution="05m",
        region=[-115, -112, 4, 6],
        registration="gridline",
        data_source="emag2_4km",
    )
    assert data.shape == (25, 37)
    assert data.lat.min() == 4
    assert data.lat.max() == 6
    assert data.lon.min() == -115
    assert data.lon.max() == -112
    npt.assert_allclose(data.min(), -128.40015)
    npt.assert_allclose(data.max(), 76.80005)


def test_earth_mag_01d_wdmam():
    """
    Test some properties of the WDMAM 01d data.
    """
    data = load_earth_magnetic_anomaly(
        resolution="01d", registration="gridline", data_source="wdmam"
    )
    assert data.name == "wdmam"
    assert data.attrs["long_name"] == "World Digital Magnetic Anomaly Map"
    assert data.attrs["units"] == "nT"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -773.5)
    npt.assert_allclose(data.max(), 1751.3)


def test_earth_mag_01d_wdmam_with_region():
    """
    Test loading low-resolution WDMAM grid with 'region'.
    """
    data = load_earth_magnetic_anomaly(
        resolution="01d",
        region=[-10, 10, -5, 5],
        registration="gridline",
        data_source="wdmam",
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -103.900024)
    npt.assert_allclose(data.max(), 102.19995)


def test_earth_mag_03m_wdmam_with_region():
    """
    Test loading a subregion of high-resolution WDMAM data.
    """
    data = load_earth_magnetic_anomaly(
        resolution="03m", region=[10, 13, -60, -58], data_source="wdmam"
    )
    assert data.gmt.registration == 0
    assert data.shape == (41, 61)
    assert data.lat.min() == -60
    assert data.lat.max() == -58
    assert data.lon.min() == 10
    assert data.lon.max() == 13
    npt.assert_allclose(data.min(), -639.7001)
    npt.assert_allclose(data.max(), 629.6)


def test_earth_mag_05m_wdmam_without_region():
    """
    Test loading a high-resolution WDMAM grid without passing 'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_magnetic_anomaly(
            resolution="05m", registration="gridline", data_source="wdmam"
        )


def test_earth_mag_wdmam_incorrect_resolution_registration():
    """
    Test that an error is raised when trying to load a WDMAM grid registration
    with an unavailable resolution.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_magnetic_anomaly(
            resolution="03m",
            region=[0, 1, 3, 5],
            registration="pixel",
            data_source="wdmam",
        )


def test_earth_mag_data_source_error():
    """
    Test that an error is raised when an invalid argument is passed to
    'data_source'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_magnetic_anomaly(resolution="01d", data_source="invalid")
