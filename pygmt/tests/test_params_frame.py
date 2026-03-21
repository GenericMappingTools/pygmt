"""
Test the Frame and Axis classes.
"""

from pygmt.params import Axis, Frame


def test_params_axis():
    """
    Test the Axis class.
    """
    assert str(Axis(annot=True)) == "a"
    assert str(Axis(annot=True, tick=True, grid=True)) == "afg"
    assert str(Axis(annot=30, tick=15, grid=5)) == "a30f15g5"
    assert str(Axis(annot=30, label="LABEL")) == "a30+lLABEL"
    assert str(Axis(annot=30, prefix="$", unit="m")) == "a30+p$+um"


def test_params_frame_only():
    """
    Test the Frame class.
    """
    assert str(Frame("WSen")) == "WSen"
    assert str(Frame(axes="WSEN", title="My Title")) == "WSEN+tMy Title"


def test_params_frame_axis():
    """
    Test the Frame class with uniform axis setting.
    """
    frame = Frame(axes="lrtb", title="My Title", axis=Axis(annot=30, tick=15, grid=10))
    assert list(frame) == ["lrtb+tMy Title", "a30f15g10"]

    frame = Frame(
        axes="WSEN",
        title="My Title",
        axis=Axis(annot=True, tick=True, grid=True, label="LABEL"),
    )
    assert list(frame) == ["WSEN+tMy Title", "afg+lLABEL"]


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
