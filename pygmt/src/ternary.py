"""
ternary - Plot data on ternary diagrams.
"""
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
    X="xshift",
    Y="yshift",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def ternary(self, data, **kwargs):
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
        Pass in either a file name to an ASCII data table, a Python list, a 2D
        {table-classes}.
    width : str
        Set the width of the figure by passing a number, followed by
        a unit (**i** for inches, **c** for centimeters). Use a negative width
        to indicate that positive axes directions be clock-wise
        [Default lets the a, b, c axes be positive in a
        counter-clockwise direction].
    {CPT}
    {G}
    style : str
        Plot symbols (including vectors, pie slices, fronts, decorated or
        quoted lines).
    {W}
    {XY}
    {U}
    {V}
    {c}
    {p}
    {t}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    with Session() as lib:
        file_context = lib.virtualfile_from_data(check_kind="vector", data=data)
        with file_context as infile:
            arg_str = " ".join([infile, build_arg_string(kwargs)])
            lib.call_module("ternary", arg_str)
