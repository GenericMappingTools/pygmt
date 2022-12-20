"""
grdcontour - Plot a contour figure.
"""
from pygmt.clib import Session
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias

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
    U="timestamp",
    V="verbose",
    W="pen",
    l="label",
    c="panel",
    f="coltypes",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(
    R="sequence", L="sequence", A="sequence_plus", c="sequence_comma", p="sequence"
)
def grdcontour(self, grid, **kwargs):
    r"""
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

        - The file name of a CPT file where the color boundaries will
          be used as contour levels.
        - The file name of a 2 (or 3) column file containing the contour
          levels (col 1), (**C**)ontour or (**A**)nnotate (col 2), and optional
          angle (col 3).
        - A fixed contour interval *cont_int* or a single contour with
          +\ *cont_int*.
    annotation : str,  int, or list
        Specify or disable annotated contour levels, modifies annotated
        contours specified in ``interval``.

        - Specify a fixed annotation interval *annot_int* or a
          single annotation level +\ *annot_int*.
        - Disable all annotation with  **-**.
        - Optional label modifiers can be specified as a single string
          ``"[annot_int]+e"``  or with a list of arguments
          ``([annot_int], "e", "f10p", "gred")``.
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
    {timestamp}
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
    >>> # load the 15 arc-minutes grid with "gridline" registration
    >>> # in a specified region
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="15m",
    ...     region=[-92.5, -82.5, -3, 7],
    ...     registration="gridline",
    ... )
    >>> # create a new plot with pygmt.Figure()
    >>> fig = pygmt.Figure()
    >>> # create the contour plot
    >>> fig.grdcontour(
    ...     # pass in the grid downloaded above
    ...     grid=grid,
    ...     # set the interval for contour lines at 250 meters
    ...     interval=250,
    ...     # set the interval for annotated contour lines at 1,000 meters
    ...     annotation=1000,
    ...     # add a frame for the plot
    ...     frame="a",
    ...     # set the projection to Mercator for the 10 cm figure
    ...     projection="M10c",
    ... )
    >>> # show the plot
    >>> fig.show()
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    with Session() as lib:
        file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
        with file_context as fname:
            lib.call_module(
                module="grdcontour", args=build_arg_string(kwargs, infile=fname)
            )
