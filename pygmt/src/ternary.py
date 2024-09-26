"""
ternary - Plot data on ternary diagrams.
"""

import pandas as pd
from packaging.version import Version
from pygmt.clib import Session, __gmt_version__
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    B="frame",
    C="cmap",
    G="fill",
    JX="width",
    R="region",
    S="style",
    V="verbose",
    W="pen",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def ternary(
    self,
    data,
    alabel: str | None = None,
    blabel: str | None = None,
    clabel: str | None = None,
    **kwargs,
):
    r"""
    Plot ternary diagrams.

    Reads (*a*,\ *b*,\ *c*\ [,\ *z*]) records from *data* and plots symbols at
    those locations on a ternary diagram. If a symbol is selected and no symbol
    size given, then we will interpret the fourth column of the input data as
    symbol size. Symbols whose *size* is <= 0 are skipped. If no symbols are
    specified then the symbol code (see ``style`` below) must be present as
    last column in the input.  If ``style`` is not specified then we instead
    plot lines or polygons.

    Full option list at :gmt-docs:`ternary.html`

    {aliases}

    Parameters
    ----------
    data : str, list, {table-like}
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
    kwargs = self._preprocess(**kwargs)

    # -Lalabel/blabel/clabel. '-' means skipping the label.
    labels = (alabel, blabel, clabel)
    if any(v is not None for v in labels):
        kwargs["L"] = "/".join(str(v) if v is not None else "-" for v in labels)

    # Patch for GMT < 6.5.0.
    # See https://github.com/GenericMappingTools/pygmt/pull/2138
    if Version(__gmt_version__) < Version("6.5.0") and isinstance(data, pd.DataFrame):
        data = data.to_numpy()

    with Session() as lib:
        with lib.virtualfile_in(check_kind="vector", data=data) as vintbl:
            lib.call_module(
                module="ternary",
                args=build_arg_list(kwargs, infile=vintbl),
            )
