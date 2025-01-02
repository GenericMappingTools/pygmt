"""
Test basic functionality for loading Earth relief datasets.
"""

import numpy as np
import numpy.testing as npt
import pytest
from packaging.version import Version
from pygmt.clib import __gmt_version__
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput


# Only test 01d and 30m to avoid downloading large datasets in CI
@pytest.mark.parametrize("data_source", ["igpp", "synbath"])
def test_earth_relief_01d_igpp_synbath(data_source):
    """
    Test some properties of the earth relief 01d data with IGPP and SYNBATH data.
    """
    data = load_earth_relief(resolution="01d", data_source=data_source)
    assert data.name == "z"
    assert data.attrs["long_name"] == "elevation (m)"
    assert data.attrs["description"] == "IGPP Earth relief"
    assert data.attrs["units"] == "meters"
    assert data.attrs["vertical_datum"] == "EGM96"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -7174.0, atol=0.5)
    npt.assert_allclose(data.max(), 5350.0, atol=0.5)


@pytest.mark.parametrize("data_source", ["gebco", "gebcosi"])
def test_earth_relief_01d_gebco(data_source):
    """
    Test some properties of the earth relief 01d data with GEBCO and GEBOCSI data.
    """
    data = load_earth_relief(resolution="01d", data_source=data_source)
    assert data.name == "z"
    assert data.attrs["long_name"] == "elevation (m)"
    assert data.attrs["description"] == "GEBCO Earth relief"
    assert data.attrs["units"] == "meters"
    assert data.attrs["vertical_datum"] == "EGM96"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -7169.0, atol=1.0)
    npt.assert_allclose(data.max(), 5350.0, atol=1.0)


def test_earth_relief_01d_with_region_srtm():
    """
    Test loading low-resolution earth relief with 'region' with IGPP data.
    """
    data = load_earth_relief(
        resolution="01d",
        region=[-10, 10, -5, 5],
        data_source="igpp",
    )
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -5118.0, atol=0.5)
    npt.assert_allclose(data.max(), 680.5, atol=0.5)


def test_earth_relief_01d_with_region_gebco():
    """
    Test loading low-resolution earth relief with 'region' with GEBCO data.
    """
    data = load_earth_relief(
        resolution="01d",
        region=[-10, 10, -5, 5],
        data_source="gebco",
    )
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -5118.0, atol=1.0)
    npt.assert_allclose(data.max(), 681.0, atol=1.0)


def test_earth_relief_30m():
    """
    Test some properties of the earth relief 30m data.
    """
    data = load_earth_relief(resolution="30m")
    assert data.shape == (361, 721)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 90.5, 0.5))
    npt.assert_allclose(data.lon, np.arange(-180, 180.5, 0.5))
    npt.assert_allclose(data.min(), -8279.5, atol=0.5)
    npt.assert_allclose(data.max(), 5544.0, atol=0.5)


def test_earth_gebcosi_15m_with_region():
    """
    Test loading a subregion of 15 arc-minutes resolution earth_gebcosi grid.
    """
    data = load_earth_relief(
        resolution="15m",
        region=[85, 87, -88, -84],
        registration="pixel",
        data_source="gebcosi",
    )
    assert data.shape == (16, 8)
    assert data.gmt.registration == 1
    npt.assert_allclose(data.lat, np.arange(-87.875, -84, 0.25))
    npt.assert_allclose(data.lon, np.arange(85.125, 87, 0.25))
    npt.assert_allclose(data.min(), -492, atol=1.0)
    npt.assert_allclose(data.max(), 435, atol=1.0)


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
    npt.assert_allclose(data.min(), -3546.5, atol=0.5)
    npt.assert_allclose(data.max(), -2282.0, atol=0.5)


def test_earth_relief_03s_landonly_srtm():
    """
    Test loading original 3 arc-seconds land-only SRTM tiles.
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
    Test loading earth relief with use_srtm=True and an incompatible data_source
    argument.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_relief(
            resolution="03s",
            region=[135, 136, 35, 36],
            registration="gridline",
            use_srtm=True,
            data_source="gebco",
        )


def test_earth_relief_15s_default_registration():
    """
    Test that the grid returned by default for the 15 arc-second resolution has a
    "pixel" registration.
    """
    data = load_earth_relief(resolution="15s", region=[-10, -9.5, 4, 5])
    assert data.shape == (240, 120)
    assert data.gmt.registration == 1
    npt.assert_allclose(data.coords["lat"].data.min(), 4.002083)
    npt.assert_allclose(data.coords["lat"].data.max(), 4.997917)
    npt.assert_allclose(data.coords["lon"].data.min(), -9.997917)
    npt.assert_allclose(data.coords["lon"].data.max(), -9.502083)
    npt.assert_allclose(data.min(), -3897, atol=0.5)
    npt.assert_allclose(data.max(), -76.5, atol=0.5)


# TODO(GMT X.Y.Z): Upstream bug which is not fixed yet.
@pytest.mark.xfail(
    condition=Version(__gmt_version__) >= Version("6.5.0"),
    reason="Upstream bug tracked in https://github.com/GenericMappingTools/pygmt/issues/2511",
)
def test_earth_relief_03s_default_registration():
    """
    Test that the grid returned by default for the 3 arc-second resolution has a
    "gridline" registration.
    """
    data = load_earth_relief(resolution="03s", region=[-10, -9.8, 4.9, 5])
    assert data.shape == (121, 241)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.coords["lat"].data.min(), 4.9)
    npt.assert_allclose(data.coords["lat"].data.max(), 5)
    npt.assert_allclose(data.coords["lon"].data.min(), -10)
    npt.assert_allclose(data.coords["lon"].data.max(), -9.8)
    npt.assert_allclose(data.min(), -2069.85, atol=0.5)
    npt.assert_allclose(data.max(), -923.5, atol=0.5)
