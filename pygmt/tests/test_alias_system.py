"""
Tests for the alias system.
"""

import pytest
from pygmt.alias import Alias, AliasSystem
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list


def func(projection=None, region=None, frame=None, label=None, text=None, **kwargs):
    """
    A simple function to test the alias system.
    """
    alias = AliasSystem(
        J=Alias(projection, name="projection"),
        R=Alias(region, name="region", separator="/", size=[4, 6]),
        B=Alias(frame, name="frame"),
        U=[Alias(label, name="label"), Alias(text, name="text", prefix="+t")],
    ).merge(kwargs)
    return build_arg_list(alias.kwdict)


def test_alias_system_one_alias():
    """
    Test that the alias system works with a single alias.
    """
    assert func(projection="X10c") == ["-JX10c"]
    assert func(projection="H10c", region=[0, 10, 0, 20]) == ["-JH10c", "-R0/10/0/20"]
    assert func(frame=["WSen", "xaf", "yaf"]) == ["-BWSen", "-Bxaf", "-Byaf"]


def test_alias_system_one_alias_short_form():
    """
    Test that the alias system works when short-form parameters coexist.
    """
    # Long-form exists but is not given, and short-form is given.
    with pytest.warns(
        SyntaxWarning,
        match="Short-form parameter 'J' is not recommended. Use long-form parameter 'projection' instead.",
    ):
        assert func(J="X10c") == ["-JX10c"]

    # Coexistence of long-form and short-form parameters.
    with pytest.raises(GMTInvalidInput, match="can't coexist"):
        func(projection="X10c", J="H10c")


def test_alias_system_multiple_aliases():
    """
    Test that the alias system works with multiple aliases.
    """
    assert func(label="abcd", text="efg") == ["-Uabcd+tefg"]


def test_alias_system_multiple_aliases_short_form():
    """
    Test that the alias system works with multiple aliases when short-form parameters
    are used.
    """
    with pytest.warns(
        SyntaxWarning,
        match="Short-form parameter 'U' is not recommended. Use long-form parameter 'label', 'text' instead.",
    ):
        assert func(U="abcd+tefg") == ["-Uabcd+tefg"]

    with pytest.raises(GMTInvalidInput, match="can't coexist"):
        func(label="abcd", U="efg")

    with pytest.raises(GMTInvalidInput, match="can't coexist"):
        func(text="efg", U="efg")
