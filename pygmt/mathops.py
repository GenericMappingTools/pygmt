"""
GMT modules for Mathematical operations on tables or grids
"""
from .clib import Session
from .exceptions import GMTInvalidInput
from .helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    C="cmap",
    G="truncate",
    H="output",
    I="reverse",
    T="series",
    V="verbose",
    Z="continuous",
)
@kwargs_to_strings(T="sequence", G="sequence")
def makecpt(**kwargs):
    """
    Make GMT color palette tables.

    This is a module that will help you make static color palette tables
    (CPTs). In classic mode we write the CPT to standard output, while under
    modern mode we simply save the CPT as the current session CPT (but see
    **output**). You define an equidistant set of contour intervals or pass
    your own z-table or list, and create a new CPT based on an existing master
    (dynamic) CPT. The resulting CPT can be reversed relative to the master
    cpt, and can be made continuous or discrete. For color tables beyond the
    standard GMT offerings, visit
    `cpt-city <http://soliton.vm.bytemark.co.uk/pub/cpt-city/>`_ and
    `Scientific Colour-Maps <http://www.fabiocrameri.ch/colourmaps.php>`_.

    The CPT includes three additional colors beyond the range of z-values.
    These are the background color (B) assigned to values lower than the lowest
    *z*-value, the foreground color (F) assigned to values higher than the
    highest *z*-value, and the NaN color (N) painted wherever values are
    undefined.

    If the master CPT includes B, F, and N entries, these will be copied into
    the new master file. If not, the parameters :gmt-term:`COLOR_BACKGROUND`,
    :gmt-term:`COLOR_FOREGROUND`, and :gmt-term:`COLOR_NAN` from the
    :gmt-docs:`gmt.conf <gmt.conf>` file or the command line will be used. This
    default behavior can be overruled using the options **-D**, **-M** or
    **-N**.

    The color model (RGB, HSV or CMYK) of the palette created by **makecpt**
    will be the same as specified in the header of the master CPT. When there
    is no :gmt-term:`COLOR_MODEL` entry in the master CPT, the
    :gmt-term:`COLOR_MODEL` specified in the :doc:`gmt.conf` file or on the
    command line will be used.

    Full option list at :gmt-docs:`makecpt.html`

    {aliases}

    Parameters
    ----------
    cmap : str
        Selects the master color palette table (CPT) to use in the
        interpolation. Full list of built-in color palette tables can be found
        at :gmt-docs:`cookbook/cpts.html#built-in-color-palette-tables-cpt`.
    series : list or str
        ``[min/max/inc[+b|l|n]|file|list]``.
        Defines the range of the new CPT by giving the lowest and highest
        z-value (and optionally an interval). If this is not given, the
        existing range in the master CPT will be used intact. The values
        produced defines the color slice boundaries.  If **+n** is used it
        refers to the number of such boundaries and not the number of slices.
        For details on array creation, see
        :gmt-docs:`makecpt.html#generate-1d-array`.
    truncate : list or str
        ``zlo/zhi``.
        Truncate the incoming CPT so that the lowest and highest z-levels are
        to *zlo* and *zhi*. If one of these equal NaN then we leave that end of
        the CPT alone. The truncation takes place before any resampling. See
        also :gmt-docs:`cookbook/features.html#manipulating-cpts`.
    output : str
        Optional. The file name with extension .cpt to store the generated CPT
        file. If not given or False (default), saves the CPT as the session
        current CPT.
    reverse : str
        Set this to True or c [Default] to reverse the sense of color
        progression in the master CPT. Set this to z to reverse the sign of
        z-values in the color table. Note that this change of z-direction
        happens before *truncate* and *series* values are used so the latter
        must be compatible with the changed *z*-range. See also
        :gmt-docs:`cookbook/features.html#manipulating-cpts`.
    continuous : bool
        Force a continuous CPT when building from a list of colors and a list
        of z-values [Default is None, i.e. discrete values].

    {V}

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
