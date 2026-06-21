"""
fill_between - Fill the area between two curves.
"""

from collections.abc import Sequence
from typing import Literal

import numpy as np
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTValueError
from pygmt.helpers import build_arg_list, fmt_docstring
from pygmt.params import Axis, Frame


@fmt_docstring
def fill_between(  # noqa: PLR0913
    self,
    x: Sequence[float],
    y: Sequence[float],
    y2: float | Sequence[float] = 0,
    x2: Sequence[float] | None = None,
    fill: str | None = None,
    pen: str | None = None,
    label: str | None = None,
    fill2: str | None = None,
    pen2: str | None = None,
    label2: str | None = None,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: Frame | Axis | Literal["none"] | str | Sequence[str] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
):
    """
    Fill the area between two horizontal curves.

    This method is a high-level wrapper around :meth:`pygmt.Figure.plot` to fill the
    area between a primary curve ``y(x)`` and a secondary curve ``y2(x)``. The ``y2``
    parameter can be either a single value [Default is 0] or a sequence. It can share
    the same ``x`` coordinates as ``y`` or use a separate ``x2`` coordinate sequence.

    Parameters
    ----------
    x
        X-coordinates of the primary curve.
    y
        Y-coordinates of the primary curve.
    y2
        Y-coordinates of the secondary curve. It can be a scalar value for a horizontal
        reference line, or a sequence with the same length as ``x`` and ``y`` when
        ``x2`` is not used. Default is 0.
    x2
        X-coordinates of the secondary curve. Use this parameter only when ``y2`` is a
        sequence sampled at different x-coordinates from ``y``. In that case, ``y2``
        must have the same length as ``x2``.
    fill
        Fill for areas where the primary curve is greater than the secondary curve.
    fill2
        Fill for areas where the secondary curve is greater than the primary curve.
    pen
        Pen attributes for the primary curve.
    pen2
        Pen attributes for the secondary curve.
    label
        Label for the primary curve, to be displayed in the legend.
    label2
        Label for the secondary curve, to be displayed in the legend.
    $projection
    $region
    $frame
    $verbose
    $panel
    $perspective
    $transparency

    Examples
    --------
    >>> import numpy as np
    >>> import pygmt
    >>> x = np.linspace(0, 2 * np.pi, 200)
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 4 * np.pi, -1.2, 1.2], projection="X10c/4c", frame=True)
    >>> fig.fill_between(
    ...     x=x,
    ...     y=np.sin(2 * x),
    ...     y2=np.sin(3 * x),
    ...     fill="lightblue",
    ...     pen="1p,blue",
    ...     fill2="lightred",
    ...     pen2="1p,red",
    ... )
    >>> fig.show()
    """
    self._activate_figure()
    _x = np.atleast_1d(x)
    _y = np.atleast_1d(y)
    _y2 = np.atleast_1d(y2)

    y2_is_scalar = np.ndim(y2) == 0

    # Validate the lengths of the input arrays
    npoints = _x.size
    if npoints <= 1:
        raise GMTValueError(
            npoints,
            description="size for 'x'/'y'",
            reason="'x' and 'y' must be arrays with lengths greater than 1.",
        )
    if _y.size != npoints:
        raise GMTValueError(
            _y.size,
            description="size for 'y'",
            reason=f"'y' is expected to have length {npoints!r}.",
        )
    if y2_is_scalar and x2 is not None:
        raise GMTValueError(
            x2,
            description="value for 'x2'",
            reason="'x2' can only be used when 'y2' is a sequence.",
        )
    if not y2_is_scalar and x2 is None and _y2.size != npoints:
        raise GMTValueError(
            _y2.size,
            description="size for 'y2'",
            reason=f"'y2' is expected to be a scalar or have length {npoints!r}.",
        )
    _x2 = None if x2 is None else np.atleast_1d(x2)
    if _x2 is not None and _y2.size != _x2.size:
        raise GMTValueError(
            _y2.size,
            description="size for 'y2'",
            reason=f"'y2' is expected to have length {_x2.size!r} when 'x2' is used.",
        )

    aliasdict = AliasSystem(
        G=Alias(fill, name="fill"),
        M=[
            Alias("s" if _x2 is not None else "c"),
            Alias(fill2, name="fill2", prefix="+g"),
            Alias(pen2, name="pen2", prefix="+p"),
            Alias(label2, name="label2", prefix="+l"),
            Alias(y2 if y2_is_scalar else None, name="y2", prefix="+y"),
        ],
        W=Alias(pen, name="pen"),
        l=Alias(label, name="label"),
    ).add_common(
        B=frame,
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )

    with Session() as lib:
        if _x2 is not None:
            with (
                lib.virtualfile_in(data={"x": _x, "y": _y}) as vintbl1,
                lib.virtualfile_in(data={"x": _x2, "y": _y2}) as vintbl2,
            ):
                lib.call_module(
                    module="plot",
                    args=build_arg_list(aliasdict, infile=[vintbl1, vintbl2]),
                )
        else:
            data = {"x": _x, "y": _y} if y2_is_scalar else {"x": _x, "y": _y, "y2": _y2}
            with lib.virtualfile_in(data=data) as vintbl:
                lib.call_module(
                    module="plot", args=build_arg_list(aliasdict, infile=vintbl)
                )
