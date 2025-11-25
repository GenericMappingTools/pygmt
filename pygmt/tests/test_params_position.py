"""
Test the Position class.
"""

from pygmt.params import Position


def test_params_position_types():
    """
    Test the Position class with different types of coordinate systems.
    """
    assert str(Position((1, 2))) == "x1/2"
    assert str(Position((10, 20), type="mapcoords")) == "g10/20"
    assert str(Position((0.1, 0.2), type="boxcoords")) == "n0.1/0.2"
    assert str(Position(("5c", "3c"), type="plotcoords")) == "x5c/3c"
    assert str(Position("TL", type="inside")) == "jTL"
    assert str(Position("BR", type="outside")) == "JBR"


def test_params_position_anchor_offset():
    """
    Test the Position class with anchor and offset parameters.
    """
    assert str(Position((10, 20), type="mapcoords", anchor="TL")) == "g10/20+jTL"

    assert str(Position((10, 20), type="mapcoords", offset=(1, 2))) == "g10/20+o1/2"

    pos = Position("TL", type="inside", anchor="MC", offset=("1c", "2c"))
    assert str(pos) == "jTL+jMC+o1c/2c"
