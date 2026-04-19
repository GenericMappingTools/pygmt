"""
ternary - Plot data on ternary diagrams.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTValueError
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias
from pygmt.params import Axis, Frame
from pygmt.params.frame import _Axes


def _ternary_frame(frame):
    """
    Convert 'frame' to ternary-compatible format.

    For ternary diagrams, GMT uses axis names **a**, **b**, **c** instead of **x**,
    **y**, **z**, and there are no primary/secondary axes. This function converts a
    :class:`pygmt.params.Frame` or :class:`pygmt.params.Axis` object to a string or
    a list of strings with the correct axis prefixes.

    Parameters
    ----------
    frame : Frame, Axis, str, list, or bool
        The frame parameter to convert.

    Returns
    -------
    str, bool, or list of str
        The converted frame parameter. For Frame inputs, returns a list of strings;
        for Axis, str, bool, or list inputs, returns the value directly.

    Examples
    --------
    >>> from pygmt.params import Axis, Frame
    >>> _ternary_frame(Axis(annot=True, tick=True, grid=True))
    ['afg', '']
    >>> _ternary_frame(
    ...     Frame(title="Title", axis=Axis(annot=True, tick=True, grid=True))
    ... )
    ['+tTitle', 'afg']
    >>> _ternary_frame(
    ...     Frame(
    ...         title="Title",
    ...         xaxis=Axis(annot=True, tick=True, grid=True, label="Water"),
    ...         yaxis=Axis(annot=True, tick=True, grid=True, label="Air"),
    ...         zaxis=Axis(annot=True, tick=True, grid=True, label="Limestone"),
    ...     )
    ... )
    ['+tTitle', 'aafg+lWater', 'bafg+lAir', 'cafg+lLimestone']
    >>> _ternary_frame(Frame(fill="lightblue", axis=Axis(annot=True)))
    ['+glightblue', 'a']
    >>> _ternary_frame("afg")
    ['afg', '']
    >>> _ternary_frame(True)
    True
    >>> _ternary_frame(["aafg+lWater", "bafg+lAir", "cafg+lLimestone"])
    ['aafg+lWater', 'bafg+lAir', 'cafg+lLimestone']
    >>> _ternary_frame("none")
    'none'
    >>> _ternary_frame(Frame(axes="WSen", axis=Axis(annot=True)))
    Traceback (most recent call last):
    pygmt.exceptions.GMTValueError: ...
    >>> _ternary_frame(Frame(xaxis2=Axis(annot=True)))
    Traceback (most recent call last):
    pygmt.exceptions.GMTValueError: ...
    """
    if isinstance(frame, Axis):
        axis_str = str(frame)
        if axis_str:
            return [axis_str, ""]
        return axis_str
    if isinstance(frame, Frame):
        _attributes = ["title", "subtitle", "fill", "axis", "xaxis", "yaxis", "zaxis"]
        if any(
            _attr not in _attributes and getattr(frame, _attr) for _attr in vars(frame)
        ):
            raise GMTValueError(
                repr(frame),
                description="frame setting",
                reason="For ternary diagrams, only Frame attributes "
                f"{', '.join(repr(_attr) for _attr in _attributes)} are supported.",
            )
        frame_settings = _Axes(
            title=frame.title, subtitle=frame.subtitle, fill=frame.fill
        )
        params = [
            Alias(frame_settings) if str(frame_settings) else Alias(None),
            Alias(frame.axis),
            Alias(frame.xaxis, prefix="a"),
            Alias(frame.yaxis, prefix="b"),
            Alias(frame.zaxis, prefix="c"),
        ]
        result = [par._value for par in params if par._value is not None]
        # When only general axis settings are used without frame-level settings
        # (title/fill) or axis-specific settings (xaxis/yaxis/zaxis), GMT needs
        # a bare -B to draw the frame border. E.g., -Bafg alone doesn't draw it.
        if not str(frame_settings) and not any((frame.xaxis, frame.yaxis, frame.zaxis)):
            result.append("")
        return result
    if isinstance(frame, str) and frame not in {"", "none", "+n"}:
        return [frame, ""]
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
    $frame
        For ternary diagrams, use :class:`pygmt.params.Frame` ``xaxis``, ``yaxis``, and
        ``zaxis`` attributes to set the **a**, **b**, and **c** axes, respectively.
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

    aliasdict = AliasSystem(
        L=Alias(labels, name="alabel/blabel/clabel", sep="/", size=3),
    ).add_common(
        B=_ternary_frame(frame),
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
