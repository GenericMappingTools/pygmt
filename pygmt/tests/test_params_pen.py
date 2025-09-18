"""
Tests for the Pen param class.
"""

from pygmt.params import Pen


def test_param_pen_width_or_color_or_style_only():
    """
    Test that Pen returns correctly formatted pen syntax when only one
    attribute (width or color or style) is given.
    """
    assert str(Pen(width=1)) == "1,,"
    assert str(Pen(color="yellow")) == ",yellow,"
    assert str(Pen(style="-.-")) == ",,-.-"


def test_param_pen_two_attributes():
    """
    Test that Pen returns correctly formatted pen syntax when two attributes
    (width/color or width/style or color/style) are given.
    """
    assert str(Pen(width=0.2, color="blue")) == "0.2,blue,"
    assert str(Pen(style="-.-", width="faint")) == "faint,,-.-"
    assert str(Pen(color="255/128/0", style="4_8_5_8:2p")) == ",255/128/0,4_8_5_8:2p"


def test_param_pen_three_attributes():
    """
    Test that Pen returns correctly formatted pen syntax when three attributes
    (width and color and style) are given.
    """
    assert str(Pen(style=".-.-", color="120-1-1", width="0.5c")) == "0.5c,120-1-1,.-.-"
