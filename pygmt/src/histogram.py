"""
Histogram - Create a histogram
"""
from pygmt.clib import Session
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    A="horizontal",
    B="frame",
    C="cmap",
    D="annotate",
    E="barwidth",
    F="center",
    G="fill",
    J="projection",
    N="normal",
    Q="cumulative",
    R="region",
    S="step",
    T="series",
    W="pen",
    X="xshift",
    Y="yshift",
    Z="type",
    c="panel",
    l="label",
    p="perspective",
)
@kwargs_to_strings(R="sequence", T="sequence")
def histogram(self, table, **kwargs):
    r"""
    Plots a histogram, and can read data from a file or
    list, array, or dataframe.

    Full option list at :gmt-docs:`histogram.html`

    {aliases}

    Parameters
    ----------
    table : str, list, or 1d array
        A data file name, list, or 1d numpy array. This is a required argument.
    {J}
    {R}
    {B}
    {CPT}
    {G}
    {W}
    {c}
    label : str
        Add a legend entry for the symbol or line being plotted.
    {p}
    horizontal : bool
        Plot the histogram using horizonal bars instead of the
        default vertical bars.
    series : int or str or list
        [*min*\ /*max*\ /]\ *inc*\ [**+n**\ ]
        Set the interval for the width of each bar in the histogram.

    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    with Session() as lib:
        file_context = lib.virtualfile_from_data(check_kind="vector", data=table)
        with file_context as infile:
            arg_str = " ".join([infile, build_arg_string(kwargs)])
            lib.call_module("histogram", arg_str)
