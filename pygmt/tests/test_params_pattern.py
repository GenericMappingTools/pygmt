"""
Test the Pattern class.
"""

import pytest
from pygmt.exceptions import GMTValueError
from pygmt.params import Pattern


def test_pattern():
    """
    Test the Pattern class.
    """
    assert str(Pattern(1)) == "p1"
    assert str(Pattern(pattern=1)) == "p1"

    assert str(Pattern("pattern.png")) == "ppattern.png"

    assert str(Pattern(10, bgcolor="red")) == "p10+bred"
    assert str(Pattern(20, fgcolor="blue")) == "p20+fblue"
    assert str(Pattern(30, bgcolor="red", fgcolor="blue")) == "p30+bred+fblue"
    assert str(Pattern(30, fgcolor="blue", bgcolor="")) == "p30+b+fblue"
    assert str(Pattern(30, fgcolor="", bgcolor="red")) == "p30+bred+f"

    assert str(Pattern(40, dpi=300)) == "p40+r300"

    assert str(Pattern(50, invert=True)) == "P50"

    pattern = Pattern(90, invert=True, bgcolor="red", fgcolor="blue", dpi=300)
    assert str(pattern) == "P90+bred+fblue+r300"

    pattern = Pattern("pattern.png", bgcolor="red", fgcolor="blue", dpi=300)
    assert str(pattern) == "ppattern.png+bred+fblue+r300"


def test_pattern_invalid_pattern():
    """
    Test that an invalid pattern number raises a GMTValueError.
    """
    with pytest.raises(GMTValueError):
        _ = str(Pattern(0))
    with pytest.raises(GMTValueError):
        _ = str(Pattern(91))


def test_pattern_invalid_colors():
    """
    Test that both fgcolor and bgcolor cannot be empty strings.
    """
    with pytest.raises(GMTValueError):
        _ = str(Pattern(10, fgcolor="", bgcolor=""))
