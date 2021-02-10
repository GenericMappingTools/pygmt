"""
grdcontour - Plot a contour figure.
"""
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    A="annotation",
    B="frame",
    C="interval",
    G="label_placement",
    J="projection",
    L="limit",
    Q="cut",
    R="region",
    S="resample",
    U="timestamp",
    V="verbose",
    W="pen",
    l="label",
    X="xshift",
    Y="yshift",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(
    R="sequence", L="sequence", A="sequence_plus", c="sequence_comma", p="sequence"
)
def grdcontour(self, grid, **kwargs):
    """
    Convert grids or images to contours and plot them on maps.

    Takes a grid file name or an xarray.DataArray object as input.

    Full option list at :gmt-docs:`grdcontour.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    interval : str or int
        Specify the contour lines to generate.

        - The filename of a `CPT`  file where the color boundaries will
          be used as contour levels.
        - The filename of a 2 (or 3) column file containing the contour
          levels (col 1), (C)ontour or (A)nnotate (col 2), and optional
          angle (col 3)
        - A fixed contour interval ``cont_int`` or a single contour with
          ``+[cont_int]``
    annotation : str,  int, or list
        Specify or disable annotated contour levels, modifies annotated
        contours specified in ``-C``.

        - Specify a fixed annotation interval ``annot_int`` or a
          single annotation level ``+[annot_int]``
        - Disable all annotation  with  ``'-'``
        - Optional label modifiers can be specified as a single string
          ``'[annot_int]+e'``  or with a list of options
          ``([annot_int], 'e', 'f10p', 'gred')``.
    limit : str or list of 2 ints
        Do no draw contours below `low` or above `high`, specify as string
        ``'[low]/[high]'``  or list ``[low,high]``.
    cut : str or int
        Do not draw contours with less than `cut` number of points.
    resample : str or int
        Resample smoothing factor.
    {J}
    {R}
    {B}
    label_placement : str
        ``[d|f|n|l|L|x|X]params``.
        The required argument controls the placement of labels along the
        quoted lines. It supports five controlling algorithms. See
        :gmt-docs:`grdcontour.html#g` for details.
    {U}
    {V}
    {W}
    {XY}
    {c}
    label : str
        Add a legend entry for the contour being plotted. Normally, the
        annotated contour is selected for the legend. You can select the
        regular contour instead, or both of them, by considering the label
        to be of the format [*annotcontlabel*][/*contlabel*]. If either
        label contains a slash (/) character then use ``|`` as the
        separator for the two labels instead.
    {p}
    {t}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    kind = data_kind(grid, None, None)
    with Session() as lib:
        if kind == "file":
            file_context = dummy_context(grid)
        elif kind == "grid":
            file_context = lib.virtualfile_from_grid(grid)
        else:
            raise GMTInvalidInput("Unrecognized data type: {}".format(type(grid)))
        with file_context as fname:
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            lib.call_module("grdcontour", arg_str)
