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
    time_window: Sequence[float] | bool = False,
    offset: float | Sequence[float] | None = None,
    profile: str | None = None,
    preprocess: str | None = None,
    fill: str | Sequence[str] | bool = False,
    amplitude_scale: float | str | Sequence[float | str] | None = None,
    vertical: bool = False,
    time_scale: float | str | None = None,
    reduction_velocity: float | None = None,
    time_shift: float | None = None,
    time_reference: Literal[
        "b",
        "e",
        "o",
        "a",
        "t0",
        "t1",
        "t2",
        "t3",
        "t4",
        "t5",
        "t6",
        "t7",
        "t8",
        "t9",
    ]
    | None = None,
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
       - E = profile
       - F = preprocess
       - G = fill
       - J = projection
       - M = amplitude_scale
       - Q = vertical
       - R = region
       - S = time_scale
       - T = **+r**: reduction_velocity, **+s**: time_shift, **+t**: time_reference
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
        the SAC header is used. Set to ``True`` to determine *t0*/*t1* from the
        *xmin*/*xmax* of the ``region`` parameter.
    offset
        Offset the seismogram positions by the given amounts *dx*[/ *dy*]
        [Default is no offset]. If *dy* is not given, it is set equal to *dx*.
    profile
        Choose the profile type, i.e., the type of the y axis. Use ``a`` for
        azimuth, ``b`` for back-azimuth, ``k`` for epicentral distance in km,
        ``d`` for epicentral distance in degrees, ``n`` for trace number (the
        first trace is numbered *n*, e.g., ``n0``), and ``u`` for user-defined
        profile (the y positions are determined by the SAC header variable
        ``usern``, e.g., ``u0``).
    preprocess
        Preprocess the data before plotting. Use ``i`` for integral, ``q`` for
        square, and ``r`` for removing the mean value. The letters can repeat
        multiple times, and the order controls the processing order, e.g.,
        ``"rii"`` converts acceleration to displacement.
    fill
        Paint the positive or negative portion of the traces. Use ``p``/``n`` to
        paint the positive/negative portion [Default paints the positive
        portion], ``+g`` *fill* to set the fill color [Default is ``"black"``],
        ``+z`` *zero* to define the zero line, and ``+t`` *t0*/*t1* to paint a
        time window only. Can be repeated to paint the positive and negative
        portions separately, e.g., ``["p+gblack", "n+gred"]``. Set to ``True``
        to paint the positive portion with the default fill.
    amplitude_scale
        Set the vertical scaling of the traces.

        - If only *size* is given (optionally with a unit), all traces are
          scaled to the given height on the map.
        - If *size*/*alpha* is given with a negative *alpha*, all traces use
          the same scaling factor determined by the first trace, which is
          scaled to *size*.
        - If *alpha* is 0, all traces are multiplied by *size* [no unit is
          allowed].
        - If *alpha* is positive, all traces are multiplied by *size* times the
          epicentral distance (in km) raised to the power *alpha*.
    vertical
        Plot traces vertically, i.e., the y axis is time and the x axis is
        amplitude.
    time_scale
        Set the time scale in seconds per unit while plotting on geographic
        plots. Append a unit (``c``, ``i``, or ``p``); if omitted, the unit is
        controlled by :gmt-term:`PROJ_LENGTH_UNIT`. Use the ``i`` prefix to give
        the reciprocal scale, i.e., unit per second.
    reduction_velocity
        Set the reduction velocity in km/s. The trace times are reduced by
        *distance*/*reduction_velocity*, where *distance* is the epicentral
        distance in the SAC header.
    time_shift
        Shift all traces by the given number of seconds.
    time_reference
        Align all traces along the given time mark. Choose from ``"b"``,
        ``"e"``, ``"o"``, ``"a"``, or ``"t0"`` to ``"t9"``.
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
        E=Alias(profile, name="profile"),
        F=Alias(preprocess, name="preprocess"),
        G=Alias(fill, name="fill"),
        M=Alias(amplitude_scale, name="amplitude_scale", sep="/", size=(1, 2)),
        Q=Alias(vertical, name="vertical"),
        S=Alias(time_scale, name="time_scale"),
        T=[
            Alias(reduction_velocity, name="reduction_velocity", prefix="+r"),
            Alias(time_shift, name="time_shift", prefix="+s"),
            Alias(
                time_reference,
                name="time_reference",
                prefix="+t",
                mapping={
                    "b": -5,
                    "e": -4,
                    "o": -3,
                    "a": -2,
                    "t0": 0,
                    "t1": 1,
                    "t2": 2,
                    "t3": 3,
                    "t4": 4,
                    "t5": 5,
                    "t6": 6,
                    "t7": 7,
                    "t8": 8,
                    "t9": 9,
                },
            ),
        ],
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
