"""
Tests for gmt.decorators
"""
import pytest

from ..decorators import kwargs_to_strings


def test_kwargs_to_strings_fails():
    "Make sure it fails for invalid conversion types."
    with pytest.raises(AssertionError):
        kwargs_to_strings(bla="blablabla")


def test_kwargs_to_strings_no_bools():
    "Test that not converting bools works"

    @kwargs_to_strings(convert_bools=False)
    def my_module(**kwargs):
        "Function that does nothing"
        return kwargs

    # The module should return the exact same arguments it was given
    args = dict(P=True, A=False, R='1/2/3/4')
    assert my_module(**args) == args
