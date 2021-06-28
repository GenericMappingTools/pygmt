"""
contour - Plot contour table data.
"""

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    deprecate_parameter,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@deprecate_parameter("columns", "incols", "v0.4.0", remove_version="v0.6.0")
@use_alias(
    A="annotation",
    B="frame",
    C="levels",
    G="label_placement",
    J="projection",
    L="triangular_mesh_pen",
    N="no_clip",
    R="region",
    S="skip",
    V="verbose",
    W="pen",
    X="xshift",
    Y="yshift",
    c="panel",
    i="incols",
    l="label",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", i="sequence_comma", p="sequence")
def contour(self, x=None, y=None, z=None, data=None, **kwargs):
    r"""
    Contour table data by direct triangulation.

    Takes a matrix, (x,y,z) pairs, or a file name as input and plots lines,
    polygons, or symbols at those locations on a map.

    Must provide either ``data`` or ``x``/``y``/``z``.

    Full option list at :gmt-docs:`contour.html`

    {aliases}

    Parameters
    ----------
    x/y/z : 1d arrays
        Arrays of x and y coordinates and values z of the data points.
    data : str or 2d array
        Either a data file name or a 2d numpy array with the tabular data.
    {J}
    {R}
    annotation : str or int
        Specify or disable annotated contour levels, modifies annotated
        contours specified in ``interval``.

        - Specify a fixed annotation interval *annot_int* or a
          single annotation level +\ *annot_int*.
    {B}
    levels : str or int
        Specify the contour lines to generate.

        - The filename of a CPT file where the color boundaries will
          be used as contour levels.
        - The filename of a 2 (or 3) column file containing the contour
          levels (col 1), (**C**)ontour or (**A**)nnotate (col 2), and optional
          angle (col 3)
        - A fixed contour interval *cont_int* or a single contour with
          +\ *cont_int*
    D : str
        Dump contour coordinates.
    E : str
        Network information.
    label_placement : str
        Placement of labels.
    I : bool
        Color the triangles using CPT.
    triangular_mesh_pen : str
        Pen to draw the underlying triangulation [Default is none].
    no_clip : bool
        Do NOT clip contours or image at the boundaries [Default will clip
        to fit inside region].
    Q : float or str
        [*cut*][**+z**].
        Do not draw contours with less than cut number of points.
    skip : bool or str
        [**p**\|\ **t**].
        Skip input points outside region.
    {W}
    label : str
        Add a legend entry for the contour being plotted. Normally, the
        annotated contour is selected for the legend. You can select the
        regular contour instead, or both of them, by considering the label
        to be of the format [*annotcontlabel*][/*contlabel*]. If either
        label contains a slash (/) character then use ``|`` as the
        separator for the two labels instead.
    {V}
    {XY}
    {c}
    {i}
    {p}
    {t}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    kind = data_kind(data, x, y, z)
    if kind == "vectors" and z is None:
        raise GMTInvalidInput("Must provided both x, y, and z.")

    with Session() as lib:
        # Choose how data will be passed in to the module
        if kind == "file":
            file_context = dummy_context(data)
        elif kind == "matrix":
            file_context = lib.virtualfile_from_matrix(data)
        elif kind == "vectors":
            file_context = lib.virtualfile_from_vectors(x, y, z)

        with file_context as fname:
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            lib.call_module("contour", arg_str)
