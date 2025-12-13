"""
Test the Position class.
"""

import pytest
from pygmt.exceptions import GMTValueError
from pygmt.params import Position


def test_params_position_cstypes():
    """
    Test the Position class with different cstypes of coordinate systems.
    """
    # Default cstype is "plotcoords" for (x,y) and "inside" for anchor codes.
    assert str(Position((1, 2))) == "x1/2"
    assert str(Position("TL")) == "jTL"

    assert str(Position((10, 20), cstype="mapcoords")) == "g10/20"
    assert str(Position((0.1, 0.2), cstype="boxcoords")) == "n0.1/0.2"
    assert str(Position(("5c", "3c"), cstype="plotcoords")) == "x5c/3c"
    assert str(Position("MR", cstype="inside")) == "jMR"
    assert str(Position("BR", cstype="outside")) == "JBR"


def test_params_position_anchor_offset():
    """
    Test the Position class with anchor and offset parameters.
    """
    assert str(Position((10, 20), cstype="mapcoords", anchor="TL")) == "g10/20+jTL"
    assert str(Position((10, 20), cstype="mapcoords", offset=(1, 2))) == "g10/20+o1/2"
    pos = Position("TL", cstype="inside", anchor="MC", offset=("1c", "2c"))
    assert str(pos) == "jTL+jMC+o1c/2c"
    assert str(Position("TL", anchor="BR", offset=0.5)) == "jTL+jBR+o0.5"


def test_params_position_invalid_location():
    """
    Test that invalid location inputs raise GMTValueError.
    """
    with pytest.raises(GMTValueError):
        Position("invalid", cstype="mapcoords")
    with pytest.raises(GMTValueError):
        Position((1, 2, 3), cstype="mapcoords")
    with pytest.raises(GMTValueError):
        Position(5, cstype="plotcoords")
    with pytest.raises(GMTValueError):
        Position((0.5,), cstype="boxcoords")
    with pytest.raises(GMTValueError):
        Position((10, 20), cstype="inside")
    with pytest.raises(GMTValueError):
        Position("TT", cstype="outside")


def test_params_position_invalid_anchor():
    """
    Test that invalid anchor inputs raise GMTValueError.
    """
    with pytest.raises(GMTValueError):
        Position((10, 20), cstype="mapcoords", anchor="XX")
