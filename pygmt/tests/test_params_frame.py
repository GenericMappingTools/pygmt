"""
Test the Frame/Axes/Axis classes.
"""

from pygmt.params import Axis, Frame


def test_params_axis():
    """
    Test the Axis class.
    """
    assert str(Axis(annotation=True)) == "a"
    assert str(Axis(annotation=True, tick=True, grid=True)) == "afg"
    assert str(Axis(annotation=1, tick=0.5, grid=0.1)) == "a1f0.5g0.1"

    assert str(Axis(annotation=1, angle=30)) == "a1+a30"
    assert str(Axis(annotation=1, angle=30, skip_edge="left")) == "a1+a30+el"
    assert str(Axis(annotation=1, fancy=True)) == "a1+f"
    assert str(Axis(annotation=1, label="My Label")) == "a1+lMy Label"
    assert str(Axis(annotation=1, hlabel="My HLabel")) == "a1+LMy HLabel"
    assert str(Axis(annotation=1, alt_label="Alt Label")) == "a1+sAlt Label"
    assert str(Axis(annotation=1, alt_hlabel="Alt HLabel")) == "a1+SAlt HLabel"
    assert str(Axis(annotation=1, prefix="$")) == "a1+p$"
    assert str(Axis(annotation=1, unit="km")) == "a1+ukm"

    axis = Axis(
        annotation=1,
        tick=0.5,
        grid=0.1,
        angle=45,
        skip_edge="right",
        fancy=True,
        label="Label",
        hlabel="HLabel",
        alt_label="AltLabel",
        alt_hlabel="AltHLabel",
        prefix="$",
        unit="m",
    )
    assert str(axis) == "a1f0.5g0.1+a45+er+f+lLabel+LHLabel+sAltLabel+SAltHLabel+p$+um"


def test_params_frame():
    """
    Test the Frame class.
    """
    # Test individual parameters of the Axes part.
    assert str(Frame(axes="WSen")) == "WSen"
    assert str(Frame(fill="red")) == "+gred"
    assert str(Frame(title="My Plot Title")) == "+tMy Plot Title"
    assert str(Frame(subtitle="My Subtitle")) == "+sMy Subtitle"
    assert str(Frame(box=True)) == "+b"
    assert str(Frame(pen="thick")) == "+wthick"
    assert str(Frame(yzfill="blue")) == "+yblue"
    assert str(Frame(xzfill="green")) == "+xgreen"
    assert str(Frame(xyfill="yellow")) == "+zyellow"
    assert str(Frame(pole=[30, -90])) == "+o30/-90"

    # Test all parameters of the Axes part.
    frame = Frame(
        axes="lrtb",
        fill="lightblue",
        title="Plot Title",
        subtitle="My Subtitle",
        box=True,
        pen="1p,blue",
        yzfill="pink",
        xzfill="orange",
        xyfill="purple",
        pole=["45N", "100W"],
    )
    assert str(frame) == (
        "lrtb+glightblue+tPlot Title+sMy Subtitle+b+w1p,blue+ypink+xorange+zpurple+o45N/100W"
    )

    # Test Frame with Axis parameters.
    frame = Frame(axis=Axis(annotation=True, tick=True))
    assert str(frame) == "af"
    frame = Frame(axis=Axis(annotation=1, tick=0.5, label="Y Axis"), title="Plot Title")
    assert str(frame) == "a1f0.5+lY Axis+tPlot Title"

    # Test Frame with separate Axis for x and y axes.
    frame = Frame(
        x=Axis(annotation=1, tick=0.5, label="X Axis"),
        y=Axis(annotation=True, tick=True, label="Y Axis"),
        axes="WSen",
        title="Plot Title",
    )
    assert list(frame) == ["xa1f0.5+lX Axis", "yaf+lY Axis", "WSen+tPlot Title"]
