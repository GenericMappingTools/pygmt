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
    data: PathLike | str | Sequence[PathLike | str],
    pen: str | None = None,
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
       - J = projection
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
    pen : str
        Set pen attributes for all traces [Default is ``"0.25p,black,solid"``].
    $projection
    $region
    $frame
    $verbose
    $panel
    $perspective
    $transparency
    """
    aliasdict = AliasSystem(
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
        lib.call_module(module="sac", args=build_arg_list(aliasdict, infile=spec))
