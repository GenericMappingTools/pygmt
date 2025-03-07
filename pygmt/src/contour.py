"""
contour - Plot contour table data.
"""

from pygmt.clib import Session
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)


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
    data : str, {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    x/y/z : 1-D arrays
        Arrays of x and y coordinates and values z of the data points.
    {projection}
    {region}
    annotation : float, list, or str
        Specify or disable annotated contour levels, modifies annotated
        contours specified in ``levels``.

        - Specify a fixed annotation interval.
        - Specify a list of annotation levels.
        - Disable all annotations by setting ``annotation="n"``.
        - Adjust the appearance by appending different modifiers, e.g.,
          ``"annot_int+f10p+gred"`` gives annotations with a font size of 10 points and
          a red filled box. For all available modifiers see :gmt-docs:`contour.html#a`.
    {frame}
    levels : float, list, or str
        Specify the contour lines to generate.

        - The file name of a CPT file where the color boundaries will be used as
          contour levels.
        - The file name of a 2 (or 3) column file containing the contour levels (col 0),
          (**C**)ontour or (**A**)nnotate (col 1), and optional angle (col 2).
        - A fixed contour interval.
        - A list of contour levels.
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
        Pen to draw the underlying triangulation [Default is ``None``].
    no_clip : bool
        Do **not** clip contours or image at the frame boundaries
        [Default is ``False`` to fit inside ``region``].
    Q : float or str
        [*cut*][**+z**].
        Do not draw contours with less than *cut* number of points.
    skip : bool or str
        [**p**\|\ **t**].
        Skip input points outside region.
    pen : str or list
        [*type*]\ *pen*\ [**+c**\ [**l**\|\ **f**]].
        *type*, if present, can be **a** for annotated contours or **c** for regular
        contours [Default]. The pen sets the attributes for the particular line.
        Default pen for annotated contours is ``"0.75p,black"`` and for regular
        contours ``"0.25p,black"``. Normally, all contours are drawn with a fixed
        color determined by the pen setting. If **+cl** is appended the colors of the
        contour lines are taken from the CPT (see ``levels``). If **+cf** is
        appended the colors from the CPT file are applied to the contour annotations.
        Select **+c** for both effects.
    label : str
        Add a legend entry for the contour being plotted. Normally, the
        annotated contour is selected for the legend. You can select the
        regular contour instead, or both of them, by considering the label
        to be of the format [*annotcontlabel*][/*contlabel*]. If either
        label contains a slash (/) character then use ``|`` as the
        separator for the two labels instead.
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
    kwargs = self._preprocess(**kwargs)

    # Specify levels for contours or annotations.
    # One level is converted to a string with a trailing comma to separate it from
    # specifying an interval.
    # Multiple levels are concatenated to a comma-separated string.
    for arg in ["A", "C"]:
        if is_nonstr_iter(kwargs.get(arg)):
            if len(kwargs[arg]) == 1:  # One level
                kwargs[arg] = str(kwargs[arg][0]) + ","
            else:  # Multiple levels
                kwargs[arg] = ",".join(f"{item}" for item in kwargs[arg])

    with Session() as lib:
        with lib.virtualfile_in(
            check_kind="vector", data=data, x=x, y=y, z=z, required_z=True
        ) as vintbl:
            lib.call_module(
                module="contour", args=build_arg_list(kwargs, infile=vintbl)
            )
