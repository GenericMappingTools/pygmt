"""
Test basic functionality for loading Earth magnetic anomaly datasets.
"""

import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_earth_magnetic_anomaly
from pygmt.exceptions import GMTInvalidInput


def test_earth_mag_01d():
    """
    Test some properties of the magnetic anomaly 01d data.
    """
    data = load_earth_magnetic_anomaly(resolution="01d")
    assert data.name == "z"
    assert data.attrs["long_name"] == "anomaly (nT)"
    assert data.attrs["description"] == "EMAG2 Earth Magnetic Anomaly Model"
    assert data.attrs["units"] == "nT"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -336.2, atol=0.2)
    npt.assert_allclose(data.max(), 517.0, atol=0.2)


def test_earth_mag_01d_with_region():
    """
    Test loading low-resolution earth magnetic anomaly with 'region'.
    """
    data = load_earth_magnetic_anomaly(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -54.4, atol=0.2)
    npt.assert_allclose(data.max(), 61.4, atol=0.2)


def test_earth_mag_02m_default_registration():
    """
    Test that the grid returned by default for the 2 arc-minute resolution has a "pixel"
    registration.
    """
    data = load_earth_magnetic_anomaly(resolution="02m", region=[-10, -9, 3, 5])
    assert data.shape == (60, 30)
    assert data.gmt.registration == 1
    npt.assert_allclose(data.coords["lat"].data.min(), 3.016666667)
    npt.assert_allclose(data.coords["lat"].data.max(), 4.983333333)
    npt.assert_allclose(data.coords["lon"].data.min(), -9.98333333)
    npt.assert_allclose(data.coords["lon"].data.max(), -9.01666667)
    npt.assert_allclose(data.min(), -231.0, atol=0.2)
    npt.assert_allclose(data.max(), 131.8, atol=0.2)


def test_earth_mag4km_01d():
    """
    Test some properties of the magnetic anomaly 4km 01d data.
    """
    data = load_earth_magnetic_anomaly(resolution="01d", data_source="emag2_4km")
    assert data.name == "z"
    assert data.attrs["long_name"] == "anomaly (nT)"
    assert data.attrs["description"] == "EMAG2 Earth Magnetic Anomaly Model"
    assert data.attrs["units"] == "nT"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -436.8, atol=0.2)
    npt.assert_allclose(data.max(), 1087.2, atol=0.2)


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
    npt.assert_allclose(data.min(), -49.6, atol=0.2)
    npt.assert_allclose(data.max(), 57.6, atol=0.2)


def test_earth_mag4km_02m_default_registration():
    """
    Test that the grid returned by default for the 2 arc-minute resolution has a "pixel"
    registration.
    """
    data = load_earth_magnetic_anomaly(
        resolution="02m",
        region=[-115, -112, 4, 6],
        data_source="emag2_4km",
    )
    assert data.shape == (60, 90)
    assert data.gmt.registration == 1
    npt.assert_allclose(data.coords["lat"].data.min(), 4.01666667)
    npt.assert_allclose(data.coords["lat"].data.max(), 5.98333333)
    npt.assert_allclose(data.coords["lon"].data.min(), -114.98333333)
    npt.assert_allclose(data.coords["lon"].data.max(), -112.01666667)
    npt.assert_allclose(data.min(), -132.8, atol=0.2)
    npt.assert_allclose(data.max(), 79.6, atol=0.2)


def test_earth_mag_01d_wdmam():
    """
    Test some properties of the WDMAM 01d data.
    """
    data = load_earth_magnetic_anomaly(
        resolution="01d", registration="gridline", data_source="wdmam"
    )
    assert data.name == "z"
    assert data.attrs["long_name"] == "anomaly (nT)"
    assert data.attrs["description"] == "WDMAM World Digital Magnetic Anomaly Map"
    assert data.attrs["units"] == "nT"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -446.6, atol=0.2)
    npt.assert_allclose(data.max(), 1330.2, atol=0.2)


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
    npt.assert_allclose(data.min(), -56.0, atol=0.2)
    npt.assert_allclose(data.max(), 55.0, atol=0.2)


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
    npt.assert_allclose(data.min(), -790.2, atol=0.2)
    npt.assert_allclose(data.max(), 528.0, atol=0.2)


def test_earth_mag_data_source_error():
    """
    Test that an error is raised when an invalid argument is passed to 'data_source'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_magnetic_anomaly(resolution="01d", data_source="invalid")
