"""
Test the Perspective class.
"""

import pytest
from pygmt.exceptions import GMTInvalidInput, GMTValueError
from pygmt.params import Perspective


def test_params_perspective():
    """
    Test the Perspective class with various parameters.
    """
    # Test azimuth, elevation, and level separately
    assert str(Perspective(azimuth=120)) == "120"
    assert str(Perspective(elevation=30)) == "180.0/30"
    assert str(Perspective(level=1000)) == "180.0/90.0/1000"

    # Test combinations of azimuth, elevation, and level
    assert str(Perspective(azimuth=120, elevation=30)) == "120/30"
    assert str(Perspective(azimuth=120, elevation=30, level=1000)) == "120/30/1000"
    assert str(Perspective(elevation=30, level=1000)) == "180.0/30/1000"

    # Test plane parameter
    assert str(Perspective(azimuth=120, elevation=30, plane="x")) == "x120/30"
    assert str(Perspective(azimuth=120, elevation=30, plane="y")) == "y120/30"
    assert str(Perspective(azimuth=120, elevation=30, plane="z")) == "z120/30"
    assert str(Perspective(plane="y")) == "y180.0"


def test_params_perspective_refpoint_cstype():
    """
    Test the Perspective class with the refpoint/cstype parameters.
    """
    # Default cstype is "mapcoords".
    assert str(Perspective(azimuth=120, refpoint=(4, 4))) == "120+w4/4"
    assert str(Perspective(azimuth=120, refpoint=(4, 4, 10))) == "120+w4/4/10"

    # Different cstype values.
    assert str(Perspective(azimuth=120, refpoint=(4, 4), cstype="mapcoords")) == (
        "120+w4/4"
    )
    assert (
        str(Perspective(azimuth=120, refpoint=(4, 4, 10), cstype="mapcoords"))
        == "120+w4/4/10"
    )
    assert str(Perspective(azimuth=120, refpoint=(4, 4), cstype="plotcoords")) == (
        "120+v4/4"
    )


def test_params_perspective_refpoint_invalid():
    """
    Test that invalid refpoint/cstype combinations raise errors.
    """
    # Invalid cstype.
    with pytest.raises(GMTValueError):
        str(Perspective(refpoint=(4, 4), cstype="bad"))
    # plotcoords ("+v") only accepts 2 values, not 3.
    with pytest.raises(GMTInvalidInput):
        str(Perspective(refpoint=(4, 4, 4), cstype="plotcoords"))


def test_params_perspective_invalid_plane():
    """
    Test that an invalid plane raises an error.
    """
    with pytest.raises(GMTValueError):
        str(Perspective(plane="bad"))
