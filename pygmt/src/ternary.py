"""
ternary - Plot data on ternary diagrams.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    B="frame",
    C="cmap",
    G="fill",
    JX="width",
    S="style",
    W="pen",
    p="perspective",
)
@kwargs_to_strings(p="sequence")
def ternary(
    self,
    data: PathLike | TableLike,
    alabel: str | None = None,
    blabel: str | None = None,
    clabel: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
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

    {aliases}
       - L = alabel/blabel/clabel
       - R = region
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    data
        Pass in either a file name to an ASCII data table, a Python list, a 2-D
        {table-classes}.
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
    {cmap}
    {fill}
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
    {pen}
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """
    self._activate_figure()

    # -Lalabel/blabel/clabel. '-' means skipping the label.
    _labels = [v if v is not None else "-" for v in (alabel, blabel, clabel)]
    labels = _labels if any(v != "-" for v in _labels) else None

    aliasdict = AliasSystem(
        L=Alias(labels, name="alabel/blabel/clabel", sep="/", size=3),
    ).add_common(
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(check_kind="vector", data=data) as vintbl:
            lib.call_module(
                module="ternary",
                args=build_arg_list(aliasdict, infile=vintbl),
            )
