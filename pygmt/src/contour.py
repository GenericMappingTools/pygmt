"""
contour - Plot contour table data.
"""

from pygmt.clib import Session
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
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
    U="timestamp",
    V="verbose",
    W="pen",
    b="binary",
    c="panel",
    d="nodata",
    e="find",
    f="coltypes",
    h="header",
    i="incols",
    l="label",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", i="sequence_comma", p="sequence")
def contour(self, data=None, x=None, y=None, z=None, **kwargs):
    r"""
    Contour table data by direct triangulation.

    Takes a matrix, (x, y, z) triplets, or a file name as input and plots,
    lines, polygons, or symbols at those locations on a map.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`contour.html`

    {aliases}

    Parameters
    ----------
    data : str or {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    x/y/z : 1-D arrays
        Arrays of x and y coordinates and values z of the data points.
    {projection}
    {region}
    annotation : str or int
        Specify or disable annotated contour levels, modifies annotated
        contours specified in ``levels``.

        - Specify a fixed annotation interval *annot_int* or a
          single annotation level +\ *annot_int*.
    {frame}
    levels : str or int
        Specify the contour lines to generate.

        - The file name of a CPT file where the color boundaries will
          be used as contour levels.
        - The file name of a 2 (or 3) column file containing the contour
          levels (col 1), (**C**)ontour or (**A**)nnotate (col 2), and optional
          angle (col 3).
        - A fixed contour interval *cont_int* or a single contour with
          +\ *cont_int*.
    D : str
        Dump contour coordinates.
    E : str
        Network information.
    label_placement : str
        [**d**\|\ **f**\|\ **n**\|\ **l**\|\ **L**\|\ **x**\|\ **X**]\ *args*.
        Control the placement of labels along the quoted lines. It supports
        five controlling algorithms. See :gmt-docs:`contour.html#g` for
        details.
    I : bool
        Color the triangles using CPT.
    triangular_mesh_pen : str
        Pen to draw the underlying triangulation [Default is None].
    no_clip : bool
        Do NOT clip contours or image at the boundaries [Default will clip
        to fit inside region].
    Q : float or str
        [*cut*][**+z**].
        Do not draw contours with less than cut number of points.
    skip : bool or str
        [**p**\|\ **t**].
        Skip input points outside region.
    {pen}
    label : str
        Add a legend entry for the contour being plotted. Normally, the
        annotated contour is selected for the legend. You can select the
        regular contour instead, or both of them, by considering the label
        to be of the format [*annotcontlabel*][/*contlabel*]. If either
        label contains a slash (/) character then use ``|`` as the
        separator for the two labels instead.
    {timestamp}
    {verbose}
    {binary}
    {panel}
    {nodata}
    {find}
    {coltypes}
    {header}
    {incols}
    {perspective}
    {transparency}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    with Session() as lib:
        # Choose how data will be passed into the module
        file_context = lib.virtualfile_from_data(
            check_kind="vector", data=data, x=x, y=y, z=z, required_z=True
        )
        with file_context as fname:
            lib.call_module(
                module="contour", args=build_arg_string(kwargs, infile=fname)
            )
