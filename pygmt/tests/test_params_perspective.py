"""
Test the Perspective class.
"""

import pytest
from pygmt.exceptions import GMTInvalidInput
from pygmt.params import Perspective


def test_params_perspective():
    """
    Test the Perspective class.
    """
    assert str(Perspective(azimuth=120)) == "120"
    assert str(Perspective(azimuth=120, elevation=30)) == "120/30"
    assert str(Perspective(azimuth=120, elevation=30, zlevel=1000)) == "120/30/1000"
    assert str(Perspective(azimuth=120, elevation=30, center=[0, 0])) == "120/30+w0/0"

    pp = Perspective(azimuth=120, elevation=30, center=(10, 20, 30))
    assert str(pp) == "120/30+w10/20/30"

    pp = Perspective(azimuth=120, elevation=30, viewpoint=[0, 0])
    assert str(pp) == "120/30+v0/0"
    assert str(Perspective(azimuth=120, elevation=30, plane="x")) == "x120/30"
    assert str(Perspective(azimuth=120, elevation=30, plane="y")) == "y120/30"
    assert str(Perspective(azimuth=120, elevation=30, plane="z")) == "z120/30"


def test_params_viewpoint_center_exclusive():
    """
    Test that center and viewpoint are mutually exclusive.
    """
    with pytest.raises(GMTInvalidInput):
        _ = str(
            Perspective(azimuth=120, elevation=30, center=(10, 20), viewpoint=(0, 0))
        )
