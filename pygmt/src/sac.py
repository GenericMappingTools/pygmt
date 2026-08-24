"""
sac - Plot seismograms in SAC format.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring
from pygmt.params import Axis, Frame


@fmt_docstring
def sac(
    self,
    data: PathLike | Sequence[PathLike],
    pen: str | None = None,
    time_window: Sequence[float] | None = None,
    offset: float | Sequence[float] | None = None,
    fill: str | None = None,
    amplitude_scale: float | str | None = None,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: Frame | Axis | Literal["none"] | str | Sequence[str] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    """
    Plot seismograms in SAC format.

    Reads SAC waveform files and plots seismic traces. Only evenly spaced SAC
    data is supported.

    Full GMT docs at :gmt-docs:`supplements/seis/sac.html`.

    **Aliases:**

    .. hlist::
       :columns: 3

       - B = frame
       - C = time_window
       - D = offset
       - G = fill
       - J = projection
       - M = amplitude_scale
       - R = region
       - V = verbose
       - W = pen
       - c = panel
       - p = perspective
       - t = transparency

    Parameters
    ----------
    data
        The SAC waveform file(s) to plot.
    pen
        Set pen attributes for all traces [Default is ``"0.25p,black,solid"``].
    time_window
        Read and plot seismograms in the time window between *t0* and *t1* only,
        where *t0* and *t1* are relative to the reference time (see
        ``time_reference``). If no reference time is set, the reference time in
        the SAC header is used.
    offset
        Offset the seismogram positions by the given amounts *dx*[/ *dy*]
        [Default is no offset]. If *dy* is not given, it is set equal to *dx*.
    fill
        Paint the positive or negative portion of the traces. Use ``p``/``n`` to
        paint the positive/negative portion [Default paints the positive
        portion], ``+g`` *fill* to set the fill color [Default is ``"black"``],
        ``+z`` *zero* to define the zero line, and ``+t`` *t0*/*t1* to paint
        a time window only.
    amplitude_scale
        Set the vertical scaling of the traces. If a unit is appended, all
        traces are scaled to the given height on the map; otherwise all traces
        are multiplied by the value.
    $projection
    $region
    $frame
    $verbose
    $panel
    $perspective
    $transparency
    """
    aliasdict = AliasSystem(
        C=Alias(time_window, name="time_window", sep="/", size=2),
        D=Alias(offset, name="offset", sep="/", size=(1, 2)),
        G=Alias(fill, name="fill"),
        M=Alias(amplitude_scale, name="amplitude_scale"),
        W=Alias(pen, name="pen"),
    ).add_common(
        B=frame,
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    self._activate_figure()
    with Session() as lib:
        lib.call_module(module="sac", args=build_arg_list(aliasdict, infile=data))
