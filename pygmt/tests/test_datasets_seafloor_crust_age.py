"""
Test basic functionality for loading Earth seafloor crust age datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_seafloor_crust_age
from pygmt.exceptions import GMTInvalidInput


def test_seafloor_crust_age_fails():
    """
    Make sure seafloor_crust_age fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_seafloor_crust_age(resolution=resolution)


# Only test 01d and 30m to avoid downloading large datasets in CI
def test_seafloor_crust_age_01d():
    """
    Test some properties of the seafloor crust age 01d data.
    """
    data = load_seafloor_crust_age(resolution="01d", registration="gridline")
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), 0.167381, rtol=1e-5)
    npt.assert_allclose(data.max(), 338.0274, rtol=1e-5)
