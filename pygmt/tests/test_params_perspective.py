"""
Test the Perspective class.
"""

import pytest
from pygmt.exceptions import GMTValueError
from pygmt.params import Perspective


def test_params_perspective():
    """
    Test the Perspective class with various parameters.
    """
    # Test azimuth, elevation, and zlevel separately
    assert str(Perspective(azimuth=120)) == "120"
    assert str(Perspective(elevation=30)) == "180.0/30"
    assert str(Perspective(zlevel=1000)) == "180.0/90.0/1000"

    # Test combinations of azimuth, elevation, and zlevel
    assert str(Perspective(azimuth=120, elevation=30)) == "120/30"
    assert str(Perspective(azimuth=120, elevation=30, zlevel=1000)) == "120/30/1000"
    assert str(Perspective(elevation=30, zlevel=1000)) == "180.0/30/1000"

    # Test plane parameter
    assert str(Perspective(azimuth=120, elevation=30, plane="x")) == "x120/30"
    assert str(Perspective(azimuth=120, elevation=30, plane="y")) == "y120/30"
    assert str(Perspective(azimuth=120, elevation=30, plane="z")) == "z120/30"
    assert str(Perspective(plane="y")) == "y180.0"


def test_params_perspective_invalid_plane():
    """
    Test that an invalid plane raises an error.
    """
    with pytest.raises(GMTValueError):
        str(Perspective(plane="bad"))
