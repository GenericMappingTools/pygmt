"""
Test the Box class.
"""

import pytest
from pygmt.exceptions import GMTInvalidInput, GMTValueError
from pygmt.params import Box


def test_params_box():
    """
    Test the Box class.
    """
    box = Box(fill="red@20")
    assert str(box) == "+gred@20"

    box = Box(clearance=(0.2, 0.2), fill="red@20", pen="blue")
    assert str(box) == "+c0.2/0.2+gred@20+pblue"

    box = Box(clearance=(0.2, 0.2), pen="blue", radius=True)
    assert str(box) == "+c0.2/0.2+pblue+r"

    box = Box(clearance=(0.1, 0.2, 0.3, 0.4), pen="blue", radius="10p")
    assert str(box) == "+c0.1/0.2/0.3/0.4+pblue+r10p"

    box = Box(
        clearance=0.2,
        pen="blue",
        radius="10p",
        shade_offset=("5p", "5p"),
        shade_fill="lightred",
    )
    assert str(box) == "+c0.2+pblue+r10p+s5p/5p/lightred"

    box = Box(clearance=0.2, inner_gap="2p", inner_pen="1p,red", pen="blue")
    assert str(box) == "+c0.2+i2p/1p,red+pblue"

    box = Box(clearance=0.2, shade_offset=("5p", "5p"), shade_fill="lightred")
    assert str(box) == "+c0.2+s5p/5p/lightred"


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
    with pytest.raises(GMTInvalidInput):
        _ = str(Box(inner_gap="2p"))
