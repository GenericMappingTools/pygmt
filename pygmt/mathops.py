"""
GMT modules for Mathematical operations on tables or grids
"""
from .clib import Session
from .exceptions import GMTInvalidInput
from .helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(C="cmap", T="series", G="truncate", H="output", I="reverse", Z="continuous")
@kwargs_to_strings(T="sequence", G="sequence")
def makecpt(**kwargs):
    """
    Creates a static color palette table (CPT).

    Full option list at :gmt-docs:`makecpt.html`

    {aliases}

    Parameters
    ----------
    cmap (C) : str
        Selects the master color palette table (CPT) to use in the
        interpolation. Full list of built-in color palette tables can be found
        at :gmt-docs:`cookbook/cpts.html#built-in-color-palette-tables-cpt`.
    series (T) : list or str
        ``[min/max/inc[+b|l|n]|file|list]``. Defines the range of the new CPT
        by giving the lowest and highest z-value (and optionally an interval).
        If this is not given, the existing range in the master CPT will be used
        intact.
    truncate (G) : list or str
        ``zlo/zhi``. Truncate the incoming CPT so that the lowest and highest
        z-levels are to zlo and zhi. If one of these equal NaN then we leave
        that end of the CPT alone. The truncation takes place before any
        resampling. See also
        :gmt-docs:`cookbook/features.html#manipulating-cpts`.
    output (H) : str
        Optional. The file name with extension .cpt to store the generated CPT
        file. If not given or False (default), saves the CPT as the session
        current CPT.
    reverse (I) : str
        Set this to True or c [Default] to reverse the sense of color
        progression in the master CPT. Set this to z to reverse the sign of
        z-values in the color table. Note that this change of z-direction
        happens before -G and -T values are used so the latter must be
        compatible with the changed z-range. See also
        :gmt-docs:`cookbook/features.html#manipulating-cpts`.
    continuous (Z) : bool
        Creates a continuous CPT [Default is discontinuous, i.e., constant
        colors for each interval]. This option has no effect when no -T is
        used, or when using -Tz_min/z_max; in the first case the input CPT
        remains untouched, in the second case it is only scaled to match the
        range z_min/z_max.

    """
    with Session() as lib:
        if "H" not in kwargs.keys():  # if no output is set
            arg_str = build_arg_string(kwargs)
        elif "H" in kwargs.keys():  # if output is set
            outfile = kwargs.pop("H")
            if not outfile or not isinstance(outfile, str):
                raise GMTInvalidInput("'output' should be a proper file name.")
            arg_str = " ".join([build_arg_string(kwargs), f"-H > {outfile}"])
        lib.call_module(module="makecpt", args=arg_str)
