"""
Test the Box class.
"""

import pytest
from pygmt.exceptions import GMTValueError
from pygmt.params import Box


def test_box_invalid_shading_offset():
    """
    Test that an invalid shading_offset raises a GMTValueError.
    """
    with pytest.raises(GMTValueError):
        _ = Box(shading_offset=("5p", "8p", "10p"))
    with pytest.raises(GMTValueError):
        _ = Box(shading_offset="10p")
