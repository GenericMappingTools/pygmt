"""
ternary - Plot data on ternary diagrams.
"""
from pygmt.clib import Session
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    B="frame",
    C="cmap",
    F="center",
    G="fill",
    JX="projection",
    R="region",
    S="style",
    U="timestamp",
    V="verbose",
    W="pen",
    X="xshift",
    Y="yshift",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", T="sequence", c="sequence_comma", p="sequence")
def ternary(self, table, **kwargs):
    r"""
    Plots a histogram, and can read data from a file or
    list, array, or dataframe.

    Full option list at :gmt-docs:`histogram.html`

    {aliases}

    Parameters
    ----------
    table : str or list or {table-like}
        Pass in either a file name to an ASCII data table, a Python list, a 2D
        {table-classes}.
    {J}
    {R}
    {CPT}
    {G}
    style : str
        Plot symbols (including vectors, pie slices, fronts, decorated or
        quoted lines).
    {W}
    {XY}
    {U}
    {V}
    {p}
    {t}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    with Session() as lib:
        file_context = lib.virtualfile_from_data(check_kind="vector", data=table)
        with file_context as infile:
            arg_str = " ".join([infile, build_arg_string(kwargs)])
            lib.call_module("ternary", arg_str)
