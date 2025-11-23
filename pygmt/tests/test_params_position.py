"""
Test the Position class.
"""

from pygmt.params import Position


def test_params_position_types():
    """
    Test the Position class with different types of coordinate systems.
    """
    assert str(Position((1, 2))) == "x1/2"
    assert str(Position(location=(1, 2))) == "x1/2"
    assert str(Position(location=(10, 20), type="mapcoords")) == "g10/20"
    assert str(Position(location=(0.1, 0.2), type="boxcoords")) == "n0.1/0.2"
    assert str(Position(location=("5c", "3c"), type="plotcoords")) == "x5c/3c"
    assert str(Position(location="TL", type="inside")) == "jTL"
    assert str(Position(location="BR", type="outside")) == "JBR"


def test_params_position_anchor_offset():
    """
    Test the Position class with anchor and offset parameters.
    """
    pos = Position(location=(10, 20), type="mapcoords", anchor="TL")
    assert str(pos) == "g10/20+jTL"

    pos = Position(location=(10, 20), type="mapcoords", offset=(1, 2))
    assert str(pos) == "g10/20+o1/2"

    pos = Position(location="TL", type="inside", anchor="MC", offset=("1c", "2c"))
    assert str(pos) == "jTL+jMC+o1c/2c"
