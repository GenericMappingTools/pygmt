"""
ternary - Plot data on ternary diagrams.
"""
import pandas as pd
from packaging.version import Version
from pygmt.clib import Session
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    B="frame",
    C="cmap",
    G="fill",
    JX="width",
    R="region",
    S="style",
    U="timestamp",
    V="verbose",
    W="pen",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def ternary(self, data, alabel=None, blabel=None, clabel=None, **kwargs):
    r"""
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
    data : str or list or {table-like}
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
    alabel : str
        Set the label for the *a* vertex where the component is 100%. The
        label is placed at a distance of three times the
        :gmt-term:`MAP_LABEL_OFFSET` setting from the corner.
    blabel : str
        Set the label for the *b* vertex where the component is 100%.
    clabel : str
        Set the label for the *c* vertex where the component is 100%.
    style : str
        *symbol*\[\ *size*].
        Plot individual symbols in a ternary diagram.
    {pen}
    {timestamp}
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    if alabel or blabel or clabel:
        alabel = str(alabel) if alabel is not None else "-"
        blabel = str(blabel) if blabel is not None else "-"
        clabel = str(clabel) if clabel is not None else "-"
        kwargs["L"] = "/".join([alabel, blabel, clabel])

    with Session() as lib:
        # Patch for GMT < 6.5.0.
        # See https://github.com/GenericMappingTools/pygmt/pull/2138
        if Version(lib.info["version"]) < Version("6.5.0") and isinstance(
            data, pd.DataFrame
        ):
            data = data.to_numpy()
        file_context = lib.virtualfile_from_data(check_kind="vector", data=data)
        with file_context as infile:
            lib.call_module(
                module="ternary",
                args=build_arg_string(kwargs, infile=infile),
            )
