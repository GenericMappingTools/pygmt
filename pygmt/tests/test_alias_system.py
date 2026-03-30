"""
Tests for the alias system.
"""

import pytest
from pygmt.alias import Alias, AliasSystem
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import build_arg_list


def func(
    projection=None,
    region=None,
    frame=None,
    label=None,
    text=None,
    offset=None,
    verbose=None,
    panel=False,
    **kwargs,
):
    """
    A simple function to test the alias system.
    """
    aliasdict = AliasSystem(
        U=[
            Alias(label, name="label"),
            Alias(text, name="text", prefix="+t"),
            Alias(offset, name="offset", prefix="+o", sep="/"),
        ],
    ).add_common(
        B=frame,
        J=projection,
        R=region,
        V=verbose,
        c=panel,
    )
    aliasdict.merge(kwargs)
    return build_arg_list(aliasdict)


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
    _msg_conflict = "Conflicting parameters: 'J' cannot be used with 'projection'."
    _msg_reason = r"Short-form parameter 'J' is not recommended. Use long-form parameter\(s\) 'projection' instead."
    # Long-form does not exist.
    assert func(A="abc") == ["-Aabc"]

    # Long-form exists but is not given, and short-form is given.
    with pytest.warns(SyntaxWarning, match=_msg_reason):
        assert func(J="X10c") == ["-JX10c"]

    # Coexistence of long-form and short-form parameters.
    with pytest.raises(GMTParameterError, match=rf"{_msg_conflict} {_msg_reason}"):
        func(projection="X10c", J="H10c")


def test_alias_system_multiple_aliases_short_form():
    """
    Test that the alias system works with multiple aliases when short-form parameters
    are used.
    """
    _msg_conflict = (
        "Conflicting parameters: 'U' cannot be used with 'label', 'text', 'offset'."
    )
    _msg_reason = r"Short-form parameter 'U' is not recommended. Use long-form parameter\(s\) 'label', 'text' \(\+t\), 'offset' \(\+o\) instead."
    # Long-form exists but is not given, and short-form is given.
    with pytest.warns(SyntaxWarning, match=_msg_reason):
        assert func(U="abcd+tefg") == ["-Uabcd+tefg"]

    # Coexistence of long-form and short-form parameters.
    with pytest.raises(GMTParameterError, match=rf"{_msg_conflict} {_msg_reason}"):
        func(label="abcd", U="efg")

    with pytest.raises(GMTParameterError, match=rf"{_msg_conflict} {_msg_reason}"):
        func(text="efg", U="efg")


def test_alias_system_common_parameter_frame():
    """
    Test that the alias system works with the 'frame' parameter.
    """
    assert func(frame="WSen") == ["-BWSen"]
    assert func(frame=["WSen", "xaf", "yaf"]) == ["-BWSen", "-Bxaf", "-Byaf"]
    assert func(frame="none") == ["-B+n"]


def test_alias_system_common_parameter_verbose():
    """
    Test that the alias system works with the 'verbose' parameter.
    """
    # Test the verbose parameter.
    assert func(verbose="quiet") == ["-Vq"]
    assert func(verbose="error") == ["-Ve"]
    assert func(verbose="warning") == ["-Vw"]
    assert func(verbose="timing") == ["-Vt"]
    assert func(verbose="info") == ["-Vi"]
    assert func(verbose="compat") == ["-Vc"]
    assert func(verbose=True) == ["-V"]
    assert func(verbose="debug") == ["-Vd"]


def test_alias_system_common_parameter_panel():
    """
    Test that the alias system works with the panel parameter.
    """
    assert func(panel=True) == ["-c"]
    assert func(panel=False) == []
    assert func(panel=(1, 2)) == ["-c1,2"]
    assert func(panel=1) == ["-c1"]
    assert func(panel="1,2") == ["-c1,2"]
