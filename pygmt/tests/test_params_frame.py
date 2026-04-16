"""
Test the Frame and Axis classes.
"""

import pytest
from pygmt.exceptions import GMTParameterError
from pygmt.params import Axis, Frame


def test_params_axis():
    """
    Test the Axis class.
    """
    assert str(Axis(annot=True)) == "a"
    assert str(Axis(annot=True, tick=True, grid=True)) == "afg"
    assert str(Axis(annot=30, tick=15, grid=5)) == "a30f15g5"
    assert str(Axis(annot=30, prefix="$", unit="m")) == "a30+p$+um"
    assert str(Axis(annot=30, label="LABEL")) == "a30+lLABEL"
    assert str(Axis(annot=30, alt_label="LABEL2")) == "a30+sLABEL2"
    assert str(Axis(annot=30, hlabel="HLABEL")) == "a30+LHLABEL"
    assert str(Axis(annot=30, alt_hlabel="HLABEL2")) == "a30+SHLABEL2"

    xaxis = Axis(annot=30, label="LABEL", alt_label="LABEL2")
    assert str(xaxis) == "a30+lLABEL+sLABEL2"
    yaxis = Axis(annot=30, hlabel="HLABEL", alt_hlabel="HLABEL2")
    assert str(yaxis) == "a30+LHLABEL+SHLABEL2"


def test_params_frame_only():
    """
    Test the Frame class.
    """
    assert str(Frame("WSen")) == "WSen"
    assert str(Frame(axes="WSEN", title="My Title")) == "WSEN+tMy Title"

    frame = Frame(axes="WSEN", title="My Title", fill="red")
    assert str(frame) == "WSEN+gred+tMy Title"

    frame = Frame(axes="WSEN", title="My Title", subtitle="My Subtitle", fill="red")
    assert str(frame) == "WSEN+gred+tMy Title+sMy Subtitle"


def test_params_frame_axis():
    """
    Test the Frame class with uniform axis setting.
    """
    frame = Frame(axes="lrtb", title="My Title", axis=Axis(annot=30, tick=15, grid=10))
    assert list(frame) == ["lrtb+tMy Title", "a30f15g10"]

    frame = Frame(
        axes="WSEN",
        title="My Title",
        subtitle="My Subtitle",
        axis=Axis(annot=True, tick=True, grid=True, label="LABEL"),
    )
    assert list(frame) == ["WSEN+tMy Title+sMy Subtitle", "afg+lLABEL"]

    frame = Frame(
        axes="WSEN",
        title="My Title",
        axis=Axis(annot=30, tick=15, grid=10),
        axis2=Axis(annot=60, tick=30, grid=20),
    )
    assert list(frame) == ["WSEN+tMy Title", "pa30f15g10", "sa60f30g20"]


def test_params_frame_separate_axes():
    """
    Test the Frame class with separate axis settings.
    """
    frame = Frame(
        xaxis=Axis(annot=10, tick=5, grid=2.5),
        yaxis=Axis(annot=20, tick=10, grid=5),
    )
    assert list(frame) == ["xa10f5g2.5", "ya20f10g5"]

    frame = Frame(
        axes="lrtb",
        title="My Title",
        xaxis=Axis(annot=10, tick=5, grid=2),
        yaxis=Axis(annot=20, tick=10, grid=4),
    )
    assert list(frame) == ["lrtb+tMy Title", "xa10f5g2", "ya20f10g4"]

    frame = Frame(
        axes="WSEN",
        title="My Title",
        xaxis=Axis(annot=True, tick=True, grid=True, label="X-LABEL"),
        yaxis=Axis(annot=True, tick=True, grid=True, label="Y-LABEL"),
    )
    assert list(frame) == ["WSEN+tMy Title", "xafg+lX-LABEL", "yafg+lY-LABEL"]


def test_params_frame_separate_axis_secondary():
    """
    Test the Frame class with separate axis settings including secondary axes.
    """
    frame = Frame(
        axes="lrtb",
        title="My Title",
        xaxis=Axis(annot=10, tick=5, grid=2),
        xaxis2=Axis(annot=15, tick=7, grid=3),
        yaxis=Axis(annot=20, tick=10, grid=4),
        yaxis2=Axis(annot=25, tick=12, grid=5),
    )
    assert list(frame) == [
        "lrtb+tMy Title",
        "pxa10f5g2",
        "pya20f10g4",
        "sxa15f7g3",
        "sya25f12g5",
    ]

    frame = Frame(
        axes="WSEN",
        title="My Title",
        xaxis=Axis(annot=True, tick=True, grid=True, label="X-LABEL"),
        yaxis=Axis(annot=True, tick=True, grid=True, label="Y-LABEL"),
    )
    assert list(frame) == ["WSEN+tMy Title", "xafg+lX-LABEL", "yafg+lY-LABEL"]


def test_params_frame_invalid_axis_combinations():
    """
    Test that invalid combinations of uniform and individual axis settings fail.
    """
    with pytest.raises(GMTParameterError, match="requires 'title'"):
        Frame(subtitle="My Subtitle")

    with pytest.raises(GMTParameterError, match="Either 'axis' or"):
        Frame(axis=Axis(annot=1), xaxis=Axis(annot=2))

    with pytest.raises(GMTParameterError, match="Either 'axis' or"):
        Frame(axis=Axis(annot=1), xaxis2=Axis(annot=2))

    with pytest.raises(GMTParameterError, match="Either 'axis2' or"):
        Frame(axis2=Axis(annot=1), xaxis=Axis(annot=2))

    with pytest.raises(GMTParameterError, match="Either 'axis2' or"):
        Frame(axis2=Axis(annot=1), yaxis2=Axis(annot=2))
