"""
GMT modules for Mathematical operations on tables or grids
"""
from .clib import Session
from .helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(C="cmap", T="series")
@kwargs_to_strings(T="sequence")
def makecpt(**kwargs):
    """
    Creates a static color palette table (CPT).

    Full option list at :gmt-docs:`makecpt.html`

    Parameters
    ----------
    cmap (C) : str
        Selects the master color palette table (CPT) to use in the interpolation.
        Full list of built-in color palette tables can be found at
        :gmt-docs:`GMT_Docs.html#built-in-color-palette-tables-cpt`.

    series (T) : list or str
        ``[min/max/inc[+b|l|n]|file|list]``.
        Defines the range of the new CPT by giving the lowest and highest z-value (and
        optionally an interval). If this is not given, the existing range in the master
        CPT will be used intact.

    {aliases}
    """
    with Session() as lib:
        arg_str = build_arg_string(kwargs)
        lib.call_module(module="makecpt", args=arg_str)
