"""
Test the Frame/Axes/Axis classes.
"""

from pygmt.params import Axes, Axis


def test_params_axis():
    """
    Test the Axis class.
    """
    assert str(Axis(interval="a1f0.5")) == "a1f0.5"
    assert str(Axis(interval="a1f0.5", angle=30)) == "a1f0.5+a30"
    assert str(Axis(interval="a1f0.5", angle=30, skip_edge="left")) == "a1f0.5+a30+el"
    assert str(Axis(interval="a1f0.5", fancy=True)) == "a1f0.5+f"
    assert str(Axis(interval="a1f0.5", label="My Label")) == "a1f0.5+lMy Label"
    assert str(Axis(interval="a1f0.5", hlabel="My HLabel")) == "a1f0.5+LMy HLabel"
    assert str(Axis(interval="a1f0.5", alt_label="Alt Label")) == "a1f0.5+sAlt Label"
    assert str(Axis(interval="a1f0.5", alt_hlabel="Alt HLabel")) == "a1f0.5+SAlt HLabel"
    assert str(Axis(interval="a1f0.5", unit="km")) == "a1f0.5+ukm"


def test_params_axes():
    """
    Test the Axes class.
    """
    assert (
        str(Axes("WSen", title="My Plot Title", fill="lightred"))
        == "WSen+glightred+tMy Plot Title"
    )
