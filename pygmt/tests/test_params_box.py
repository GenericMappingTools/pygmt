"""
Test the Box class.
"""

import pytest
from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.params import Box


def test_params_box():
    """
    Test the Box class.
    """
    assert str(Box(clearance=0.1)) == "+c0.1"
    assert str(Box(clearance=(0.1, 0.2))) == "+c0.1/0.2"
    assert str(Box(clearance=(0.1, 0.2, 0.3, 0.4))) == "+c0.1/0.2/0.3/0.4"

    assert str(Box(fill="red@20")) == "+gred@20"

    assert str(Box(pen="blue")) == "+pblue"

    assert str(Box(radius=True)) == "+r"
    assert str(Box(radius="10p")) == "+r10p"

    assert str(Box(inner_gap="2p", inner_pen="1p,red")) == "+i2p/1p,red"

    assert str(Box(shade_offset=("5p", "5p"))) == "+s5p/5p"
    assert str(Box(shade_fill="red")) == "+sred"
    assert str(Box(shade_offset=("5p", "5p"), shade_fill="red")) == "+s5p/5p/red"

    box = Box(
        clearance=0.2,
        fill="red@20",
        pen="blue",
        inner_gap="2p",
        inner_pen="1p,red",
        radius="10p",
        shade_offset=("5p", "5p"),
        shade_fill="lightred",
    )
    assert str(box) == "+c0.2+gred@20+i2p/1p,red+pblue+r10p+s5p/5p/lightred"


def test_params_box_invalid_shade_offset():
    """
    Test that an invalid shade_offset raises a GMTValueError.
    """
    with pytest.raises(GMTValueError):
        _ = str(Box(shade_offset=("5p", "8p", "10p")))
    with pytest.raises(GMTValueError):
        _ = str(Box(shade_offset="10p"))


def test_params_box_invalid_innerborder():
    """
    Test that inner_pen is required when inner_gap is set.
    """
    with pytest.raises(GMTParameterError):
        _ = str(Box(inner_gap="2p"))
