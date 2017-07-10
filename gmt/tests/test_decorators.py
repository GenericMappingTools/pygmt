"""
Tests for gmt.decorators
"""
import pytest

from ..decorators import kwargs_to_strings


def test_kwargs_to_strings_fails():
    "Make sure it fails for invalid conversion types."
    with pytest.raises(AssertionError):
        kwargs_to_strings(bla="blablabla")
