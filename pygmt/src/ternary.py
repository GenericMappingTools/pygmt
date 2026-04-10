"""
ternary - Plot data on ternary diagrams.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias
from pygmt.params import Axis, Frame


def _ternary_frame(frame):
    """
    Convert a Frame/Axis parameter to ternary-compatible format.

    For ternary diagrams, GMT uses axis names **a**, **b**, **c** instead of
    **x**, **y**, **z**, and there are no primary/secondary axes. This function
    converts a :class:`pygmt.params.Frame` or :class:`pygmt.params.Axis` object
    to a list of strings with the correct ternary prefixes.

    Parameters
    ----------
    frame : Frame, Axis, str, list, or bool
        The frame parameter to convert.

    Returns
    -------
    str, list of str, or bool
        The converted frame parameter.

    Examples
    --------
    >>> from pygmt.params import Axis, Frame
    >>> _ternary_frame(Axis(annot=True, tick=True, grid=True))
    'afg'
    >>> _ternary_frame(Axis(annot=True, tick=True))
    'af'
    >>> _ternary_frame(Frame(title="Title", axis=Axis(annot=True, tick=True, grid=True)))
    ['+tTitle', 'afg']
    >>> _ternary_frame(Frame(
    ...     title="Title",
    ...     xaxis=Axis(annot=True, tick=True, grid=True, label="Water"),
    ...     yaxis=Axis(annot=True, tick=True, grid=True, label="Air"),
    ...     zaxis=Axis(annot=True, tick=True, grid=True, label="Limestone"),
    ... ))
    ['+tTitle', 'aafg+lWater', 'bafg+lAir', 'cafg+lLimestone']
    >>> _ternary_frame("afg")
    'afg'
    >>> _ternary_frame(True)
    True
    >>> _ternary_frame(["afg", "aafg+lWater"])
    ['afg', 'aafg+lWater']
    >>> _ternary_frame(Frame(axes="WSen", axis=Axis(annot=True)))
    Traceback (most recent call last):
    pygmt.exceptions.GMTParameterError: ...
    >>> _ternary_frame(Frame(xaxis2=Axis(annot=True)))
    Traceback (most recent call last):
    pygmt.exceptions.GMTParameterError: ...
    """
    if isinstance(frame, Axis):
        return str(frame)
    if isinstance(frame, Frame):
        if frame.axes:
            raise GMTParameterError(
                conflicts_with=("frame", ["frame.axes"]),
                reason="For ternary diagrams, Frame.axes (e.g., 'WSen') is not supported.",
            )
        if any((frame.xaxis2, frame.yaxis2, frame.zaxis2)):
            raise GMTParameterError(
                conflicts_with=(
                    "frame",
                    ["frame.xaxis2", "frame.yaxis2", "frame.zaxis2"],
                ),
                reason="For ternary diagrams, secondary axes are not supported.",
            )
        parts = []
        if frame.title:
            parts.append(f"+t{frame.title}")
        # Uniform axis setting (applies to all three ternary axes)
        if frame.axis:
            parts.append(str(frame.axis))
        # Per-axis: xaxis→a, yaxis→b, zaxis→c
        for ternary_prefix, axis_obj in [
            ("a", frame.xaxis),
            ("b", frame.yaxis),
            ("c", frame.zaxis),
        ]:
            if axis_obj:
                parts.append(f"{ternary_prefix}{axis_obj}")
        return parts
    return frame


@fmt_docstring
@use_alias(C="cmap", G="fill", JX="width", S="style", W="pen")
def ternary(  # noqa: PLR0913
    self,
    data: PathLike | TableLike,
    alabel: str | None = None,
    blabel: str | None = None,
    clabel: str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: str | Sequence[str] | Literal["none"] | bool | Frame | Axis = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot data on ternary diagrams.

    Reads (*a*,\ *b*,\ *c*\ [,\ *z*]) records from *data* and plots symbols at
    those locations on a ternary diagram. If a symbol is selected and no symbol
    size given, then we will interpret the fourth column of the input data as
    symbol size. Symbols whose *size* is <= 0 are skipped. If no symbols are
    specified then the symbol code (see ``style`` below) must be present as
    last column in the input.  If ``style`` is not specified then we instead
    plot lines or polygons.

    Full GMT docs at :gmt-docs:`ternary.html`.

    $aliases
       - B = frame
       - L = alabel/blabel/clabel
       - R = region
       - V = verbose
       - c = panel
       - p = perspective
       - t = transparency

    Parameters
    ----------
    data
        Pass in either a file name to an ASCII data table, a Python list, a 2-D
        $table_classes.
    width : str
        Set the width of the figure by passing a number, followed by
        a unit (**i** for inches, **c** for centimeters). Use a negative width
        to indicate that positive axes directions be clock-wise
        [Default lets the a, b, c axes be positive in a
        counter-clockwise direction].
    region : str or list
        [*amin*, *amax*, *bmin*, *bmax*, *cmin*, *cmax*].
        Give the min and max limits for each of the three axes **a**, **b**,
        and **c**.
    $cmap
    $fill
    alabel
        Set the label for the *a* vertex where the component is 100%. The label is
        placed at a distance of three times the :gmt-term:`MAP_LABEL_OFFSET` setting
        from the corner.
    blabel
        Same as ``alabel`` but for the *b* vertex.
    clabel
        Same as ``alabel`` but for the *c* vertex.
    style : str
        *symbol*\[\ *size*].
        Plot individual symbols in a ternary diagram.
    $pen
    $verbose
    $panel
    $perspective
    $transparency
    """
    self._activate_figure()

    # -Lalabel/blabel/clabel. '-' means skipping the label.
    _labels = [v if v is not None else "-" for v in (alabel, blabel, clabel)]
    labels = _labels if any(v != "-" for v in _labels) else None

    # Convert Frame/Axis to ternary-compatible format.
    frame = _ternary_frame(frame)

    aliasdict = AliasSystem(
        L=Alias(labels, name="alabel/blabel/clabel", sep="/", size=3),
    ).add_common(
        B=frame,
        R=region,
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(check_kind="vector", data=data) as vintbl:
            lib.call_module(
                module="ternary",
                args=build_arg_list(aliasdict, infile=vintbl),
            )
