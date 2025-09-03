"""
Test the Box class.
"""

import pytest
from pygmt.exceptions import GMTValueError, GMTInvalidInput
from pygmt.params import Box


def test_params_box_invalid_shading_offset():
    """
    Test that an invalid shading_offset raises a GMTValueError.
    """
    with pytest.raises(GMTValueError):
        _ = str(Box(shading_offset=("5p", "8p", "10p")))
    with pytest.raises(GMTValueError):
        _ = str(Box(shading_offset="10p"))


def test_params_box_invalid_innerborder():
    """
    Test that inner_pen is required when inner_gap is set.
    """
    with pytest.raises(GMTInvalidInput):
        _ = str(Box(inner_gap="2p"))
