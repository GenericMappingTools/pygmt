"""
Test the Frame/Axes/Axis classes.
"""

from pygmt.params import Axes, Axis


def test_params_axis_intervals():
    """
    Test the annotation, tick, and grid parameters of the Axis class.
    """
    assert str(Axis(annotation=1)) == "a1"
    assert str(Axis(tick=2)) == "f2"
    assert str(Axis(grid=3)) == "g3"
    assert str(Axis(annotation=1, tick=2, grid=3)) == "a1f2g3"

    assert str(Axis(annotation=True)) == "a"
    assert str(Axis(tick=True)) == "f"
    assert str(Axis(grid=True)) == "g"
    assert str(Axis(annotation=True, tick=True)) == "af"
    assert str(Axis(annotation=True, grid=True)) == "ag"
    assert str(Axis(tick=True, grid=True)) == "fg"
    assert str(Axis(annotation=True, tick=True, grid=True)) == "afg"


def test_params_axis_modifiers():
    """
    Test the modifiers of the Axis class.
    """
    assert str(Axis(annotation=True, angle=30)) == "a+a30"
    assert str(Axis(annotation=True, angle="normal")) == "a+an"
    assert str(Axis(annotation=True, angle="parallel")) == "a+ap"

    assert str(Axis(annotation=True, skip_edge=True)) == "a+e"
    assert str(Axis(annotation=True, skip_edge="lower")) == "a+el"
    assert str(Axis(annotation=True, skip_edge="upper")) == "a+eu"

    assert str(Axis(annotation=True, fancy=True)) == "a+f"

    assert str(Axis(annotation=True, label="My Label")) == "a+lMy Label"
    assert str(Axis(annotation=True, hlabel="My HLabel")) == "a+LMy HLabel"
    assert str(Axis(annotation=True, alt_label="Alt Label")) == "a+sAlt Label"
    assert str(Axis(annotation=True, alt_hlabel="Alt HLabel")) == "a+SAlt HLabel"

    axis = Axis(annotation=True, label="My Label", alt_label="My HLabel")
    assert str(axis) == "a+lMy Label+sMy HLabel"

    assert str(Axis(annotation=True, prefix="$")) == "a+p$"

    assert str(Axis(annotation=True, unit="km")) == "a+ukm"


def test_params_axes():
    """
    Test the Axes class.
    """

    assert str(Axes(axes="WSen")) == "WSen"
    assert str(Axes(fill="lightred")) == "+glightred"
    assert str(Axes(title="My Plot Title")) == "+tMy Plot Title"
    assert str(Axes(subtitle="My Subtitle")) == "+sMy Subtitle"

    axes = Axes(axes="WSen", fill="lightred", title="My Plot Title")
    assert str(axes) == "WSen+glightred+tMy Plot Title"


def test_params_frame():
    """
    Test the Frame class.
    """
