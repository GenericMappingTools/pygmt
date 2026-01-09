"""
Test the Frame/Axes/Axis classes.
"""

from pygmt.params import Axis, Frame


def test_params_axis():
    """
    Test the Axis class.
    """
    assert str(Axis(annotation=1, tick=0.5)) == "a1f0.5"
    assert str(Axis(annotation=1, tick=0.5, angle=30)) == "a1f0.5+a30"
    assert (
        str(Axis(annotation=1, tick=0.5, angle=30, skip_edge="left")) == "a1f0.5+a30+el"
    )
    assert str(Axis(annotation=1, tick=0.5, fancy=True)) == "a1f0.5+f"
    assert str(Axis(annotation=1, tick=0.5, label="My Label")) == "a1f0.5+lMy Label"
    assert str(Axis(annotation=1, tick=0.5, hlabel="My HLabel")) == "a1f0.5+LMy HLabel"
    assert (
        str(Axis(annotation=1, tick=0.5, alt_label="Alt Label")) == "a1f0.5+sAlt Label"
    )
    assert (
        str(Axis(annotation=1, tick=0.5, alt_hlabel="Alt HLabel"))
        == "a1f0.5+SAlt HLabel"
    )
    assert str(Axis(annotation=1, tick=0.5, unit="km")) == "a1f0.5+ukm"


def test_params_frame():
    """
    Test the Frame class.
    """
    frame = Frame(axes="WSen")
    assert str(frame) == "WSen"

    frame = Frame(title="My Plot Title")
    assert str(frame) == "+tMy Plot Title"

    frame = Frame(subtitle="My Subtitle")
    assert str(frame) == "+sMy Subtitle"

    frame = Frame(fill="red")
    assert str(frame) == "+gred"

    frame = Frame(fill="lightblue", title="Plot Title", subtitle="My Subtitle")
    assert str(frame) == "+glightblue+tPlot Title+sMy Subtitle"

    frame = Frame(
        axes="WSen", fill="lightblue", title="Plot Title", subtitle="My Subtitle"
    )
    assert str(frame) == "WSen+glightblue+tPlot Title+sMy Subtitle"

    frame = Frame(
        x=Axis(annotation=1, tick=0.5), y=Axis(label="Y Axis"), title="Plot Title"
    )
    assert list(frame) == ["xa1f0.5", "y+lY Axis", "+tPlot Title"]

    frame = Frame(
        axis=Axis(annotation=1, tick=0.5, label="Label", angle=30), title="Plot Title"
    )
    assert list(frame) == ["a1f0.5+a30+lLabel", "+tPlot Title"]
