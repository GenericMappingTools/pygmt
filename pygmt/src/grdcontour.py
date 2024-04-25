"""
grdcontour - Plot a contour figure.
"""

from pygmt.clib import Session
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)

__doctest_skip__ = ["grdcontour"]


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
    V="verbose",
    W="pen",
    l="label",
    c="panel",
    f="coltypes",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", L="sequence", c="sequence_comma", p="sequence")
def grdcontour(self, grid, **kwargs):
    r"""
    Convert grids or images to contours and plot them on maps.

    Takes a grid file name or an xarray.DataArray object as input.

    Full option list at :gmt-docs:`grdcontour.html`

    {aliases}

    Parameters
    ----------
    {grid}
    interval : float, list, or str
        Specify the contour lines to generate.

        - The file name of a CPT file where the color boundaries will be used as
          contour levels
        - The file name of a 2 (or 3) column file containing the contour levels (col 0),
          (**C**)ontour or (**A**)nnotate (col 1), and optional angle (col 2)
        - A fixed contour interval
        - A list of contour levels
    annotation : float, list, or str
        Specify or disable annotated contour levels, modifies annotated
        contours specified in ``interval``.

        - Specify a fixed annotation interval
        - Specify a list of annotation levels
        - Disable all annotations by setting ``annotation="n"``.
        - Adjust the appearance by appending different modifiers, e.g.,
          ``"annot_int+f10p+gred"`` gives annotations with a font size of 10 points
          and a red filled box. For all available modifiers see
          :gmt-docs:`grdcontour.html#a`.
    limit : str or list of 2 ints
        *low*/*high*.
        Do no draw contours below `low` or above `high`, specify as string
    cut : str or int
        Do not draw contours with less than `cut` number of points.
    resample : str or int
        Resample smoothing factor.
    {projection}
    {region}
    {frame}
    label_placement : str
        [**d**\|\ **f**\|\ **n**\|\ **l**\|\ **L**\|\ **x**\|\ **X**]\
        *args*.
        Control the placement of labels along the quoted lines. It supports
        five controlling algorithms. See :gmt-docs:`grdcontour.html#g` for
        details.
    {verbose}
    {pen}
    {panel}
    {coltypes}
    label : str
        Add a legend entry for the contour being plotted. Normally, the
        annotated contour is selected for the legend. You can select the
        regular contour instead, or both of them, by considering the label
        to be of the format [*annotcontlabel*][/*contlabel*]. If either
        label contains a slash (/) character then use ``|`` as the
        separator for the two labels instead.
    {perspective}
    {transparency}

    Example
    -------
    >>> import pygmt
    >>> # Load the 15 arc-minutes grid with "gridline" registration in the
    >>> # specified region
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="15m",
    ...     region=[-92.5, -82.5, -3, 7],
    ...     registration="gridline",
    ... )
    >>> # Create a new plot with pygmt.Figure()
    >>> fig = pygmt.Figure()
    >>> # Create the contour plot
    >>> fig.grdcontour(
    ...     # Pass in the grid downloaded above
    ...     grid=grid,
    ...     # Set the interval for contour lines at 250 meters
    ...     interval=250,
    ...     # Set the interval for annotated contour lines at 1,000 meters
    ...     annotation=1000,
    ...     # Add a frame for the plot
    ...     frame="a",
    ...     # Set the projection to Mercator for the 10 cm figure
    ...     projection="M10c",
    ... )
    >>> # Show the plot
    >>> fig.show()
    """
    kwargs = self._preprocess(**kwargs)

    for arg in ["A", "C"]:
        if is_nonstr_iter(kwargs.get(arg)):
            if len(kwargs[arg]) == 1:
                kwargs[arg] = str(kwargs[arg][0]) + ","
            else:
                kwargs[arg] = ",".join(f"{item}" for item in kwargs[arg])

    with Session() as lib:
        with lib.virtualfile_in(check_kind="raster", data=grid) as vingrd:
            lib.call_module(
                module="grdcontour", args=build_arg_list(kwargs, infile=vingrd)
            )
