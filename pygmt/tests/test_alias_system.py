"""
Tests for the alias system.
"""

import pytest
from pygmt.alias import Alias, AliasSystem
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list


def func(
    projection=None,
    region=None,
    frame=None,
    label=None,
    text=None,
    offset=None,
    **kwargs,
):
    """
    A simple function to test the alias system.
    """
    alias = AliasSystem(
        J=Alias(projection, name="projection"),
        R=Alias(region, name="region", separator="/", size=[4, 6]),
        B=Alias(frame, name="frame"),
        U=[
            Alias(label, name="label"),
            Alias(text, name="text", prefix="+t"),
            Alias(offset, name="offset", prefix="+o", separator="/"),
        ],
    ).update(kwargs)
    return build_arg_list(alias.kwdict)


def test_alias_system_long_form():
    """
    Test that the alias system works with long-form parameters.
    """
    # One parameter
    assert func(projection="X10c") == ["-JX10c"]
    # Multiple parameters.
    assert func(projection="H10c", region=[0, 10, 0, 20]) == ["-JH10c", "-R0/10/0/20"]
    # Repeatable parameters.
    assert func(frame=["WSen", "xaf", "yaf"]) == ["-BWSen", "-Bxaf", "-Byaf"]
    # Multiple long-form parameters.
    assert func(label="abcd", text="efg", offset=(12, 12)) == ["-Uabcd+tefg+o12/12"]
    assert func(
        projection="H10c",
        region=[0, 10, 0, 20],
        label="abcd",
        text="efg",
        offset=(12, 12),
        frame=["WSen", "xaf", "yaf"],
    ) == ["-BWSen", "-Bxaf", "-Byaf", "-JH10c", "-R0/10/0/20", "-Uabcd+tefg+o12/12"]


def test_alias_system_one_alias_short_form():
    """
    Test that the alias system works when short-form parameters coexist.
    """
    # Long-form does not exist.
    assert func(A="abc") == ["-Aabc"]

    # Long-form exists but is not given, and short-form is given.
    with pytest.warns(
        SyntaxWarning,
        match="Short-form parameter 'J' is not recommended. Use long-form parameter 'projection' instead.",
    ):
        assert func(J="X10c") == ["-JX10c"]

    # Coexistence of long-form and short-form parameters.
    with pytest.raises(
        GMTInvalidInput,
        match="Short-form parameter 'J' conflicts with long-form parameters and is not recommended. Use long-form parameter 'projection' instead.",
    ):
        func(projection="X10c", J="H10c")


def test_alias_system_multiple_aliases_short_form():
    """
    Test that the alias system works with multiple aliases when short-form parameters
    are used.
    """
    _msg_long = r"Use long-form parameters 'label', with optional parameters 'text' \(\+t\), 'offset' \(\+o\) instead."
    # Long-form exists but is not given, and short-form is given.
    msg = rf"Short-form parameter 'U' is not recommended. {_msg_long}"
    with pytest.warns(SyntaxWarning, match=msg):
        assert func(U="abcd+tefg") == ["-Uabcd+tefg"]

    # Coexistence of long-form and short-form parameters.
    msg = rf"Short-form parameter 'U' conflicts with long-form parameters and is not recommended. {_msg_long}"
    with pytest.raises(GMTInvalidInput, match=msg):
        func(label="abcd", U="efg")

    with pytest.raises(GMTInvalidInput, match=msg):
        func(text="efg", U="efg")
