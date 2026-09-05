"""
sac - Plot seismograms in SAC format.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTValueError
from pygmt.helpers import build_arg_list, fmt_docstring
from pygmt.params import Axis, Frame


@fmt_docstring
def sac(
    self,
    data: PathLike | Sequence[PathLike],
    pen: str | None = None,
    time_window: Sequence[float] | bool = False,
    offset: float | Sequence[float] | None = None,
    profile: Literal[
        "azimuth",
        "back_azimuth",
        "distance_in_km",
        "distance_in_degree",
        "trace_number",
        "user0",
        "user1",
        "user2",
        "user3",
        "user4",
        "user5",
        "user6",
        "user7",
        "user8",
        "user9",
    ]
    | None = None,
    trace_number: int | None = None,
    preprocess: str | None = None,
    positive_fill: str | None = None,
    negative_fill: str | None = None,
    fill_zero: float | None = None,
    fill_time_window: Sequence[float] | None = None,
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
       - E = profile, trace_number
       - F = preprocess
       - G = positive_fill, negative_fill, fill_zero, fill_time_window
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
        Choose the profile type, i.e., the type of the y axis. Choose from
        ``"azimuth"``, ``"back_azimuth"``, ``"distance_in_km"``,
        ``"distance_in_degree"``, ``"trace_number"``, or ``"user0"`` to
        ``"user9"``. User-defined profiles use the corresponding SAC header
        variable, e.g., ``"user0"`` uses ``user0``.
    trace_number
        Set the number of the first trace for a trace-number profile. If not
        specified, the first trace is numbered 0.
    preprocess
        Preprocess the data before plotting. Use ``i`` for integral, ``q`` for
        square, and ``r`` for removing the mean value. The letters can repeat
        multiple times, and the order controls the processing order, e.g.,
        ``"rii"`` converts acceleration to displacement.
    positive_fill
        Set the color or pattern for filling the positive portion of the traces.
    negative_fill
        Set the color or pattern for filling the negative portion of the traces.
    fill_zero
        Set the zero line for ``positive_fill`` and ``negative_fill``.
    fill_time_window
        Set the time window *t0*/*t1* for ``positive_fill`` and
        ``negative_fill``.
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
    if profile is not None and trace_number is not None:
        raise GMTValueError(
            [profile, trace_number],
            description="parameters 'profile' and 'trace_number'",
            reason="Only one can be specified.",
        )

    profile_mapping = {
        "azimuth": "a",
        "back_azimuth": "b",
        "distance_in_km": "k",
        "distance_in_degree": "d",
        "trace_number": "n",
        **{f"user{number}": f"u{number}" for number in range(10)},
    }
    profile_alias = (
        Alias(trace_number, name="trace_number", prefix="n")
        if trace_number is not None
        else Alias(profile, name="profile", mapping=profile_mapping)
    )

    fill_modifiers = "".join(
        modifier
        for modifier in (
            Alias(fill_zero, name="fill_zero", prefix="+z")._value,
            Alias(
                fill_time_window,
                name="fill_time_window",
                prefix="+t",
                sep="/",
                size=2,
            )._value,
        )
        if modifier is not None
    )
    fill_options = [
        f"p+g{positive_fill}{fill_modifiers}" if positive_fill is not None else None,
        f"n+g{negative_fill}{fill_modifiers}" if negative_fill is not None else None,
    ]
    if fill_modifiers and not any(fill_options):
        raise GMTValueError(
            [fill_zero, fill_time_window],
            description="parameters 'fill_zero' and 'fill_time_window'",
            reason="At least one of 'positive_fill' or 'negative_fill' must be specified.",
        )

    aliasdict = AliasSystem(
        C=Alias(time_window, name="time_window", sep="/", size=2),
        D=Alias(offset, name="offset", sep="/", size=(1, 2)),
        E=profile_alias,
        F=Alias(preprocess, name="preprocess"),
        G=Alias([option for option in fill_options if option is not None], name="fill"),
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
