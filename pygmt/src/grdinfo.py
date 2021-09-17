"""
grdinfo - Retrieve info about grid file.
"""
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    C="per_column",
    D="tiles",
    F="geographic",
    I="spacing",
    L="force_scan",
    M="minmax_pos",
    R="region",
    T="nearest_multiple",
    V="verbose",
    f="coltypes",
)
@kwargs_to_strings(D="sequence", I="sequence", R="sequence")
def grdinfo(grid, **kwargs):
    r"""
    Get information about a grid.

    Can read the grid from a file or given as an xarray.DataArray grid.

    Full option list at :gmt-docs:`grdinfo.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
        This is the only required parameter.
    {R}
    per_column : str or bool
        **n**\|\ **t**.
        Formats the report using tab-separated fields on a single line. The
        output is name *w e s n z0 z1 dx dy nx ny* [ *x0 y0 x1 y1* ]
        [ *med scale* ] [ *mean std rms* ] [ *n_nan* ] *registration gtype*.
        The data in brackets are outputted depending on the ``force_scan``
        and ``minmax_pos`` parameters. Use **t** to place file name at the end
        of the output record or, **n** or ``True`` to only output numerical
        columns. The registration is either 0 (gridline) or 1 (pixel), while
        gtype is either 0 (Cartesian) or 1 (geographic). The default value is
        ``False``. This cannot be called if ``geographic`` is also set.
    tiles : str or list
        *xoff*\ [/*yoff*][**+i**].
        Divide a single grid's domain (or the ``region`` domain, if no grid
        given) into tiles of size dx times dy (set via ``spacing``). You can
        specify overlap between tiles by appending *xoff*\ [/*yoff*]. If the
        single grid is given you may use the modifier **+i** to ignore tiles
        that have no data within each tile subregion. Default output is text
        region strings. Use ``per_column`` to instead report four columns with
        xmin xmax ymin ymax per tile, or use ``per_column="t"`` to also have
        the region string appended as trailing text.
    geographic : bool
        Report grid domain and x/y-increments in world mapping format
        The default value is ``False``. This cannot be called if
        ``per_column`` is also set.
    spacing : str or list
        *dx*\ [/*dy*]\|\ **b**\|\ **i**\|\ **r**.
        Report the min/max of the region to the nearest multiple of dx and dy,
        and output this in the form w/e/s/n (unless ``per_column`` is set). To
        report the actual grid region, append **r**. For a grid produced by
        the img supplement (a Cartesian Mercator grid), the exact geographic
        region is given with **i** (if not found then we return the actual
        grid region instead). If no argument is given then we report the grid
        increment in the form *xinc*\ [/*yinc*]. If **b** is given we write
        each grid's bounding box polygon instead. Finally, if ``tiles`` is in
        effect then *dx* and *dy* are the dimensions of the desired tiles.
    force_scan : int or str
        **0**\|\ **1**\|\ **2**\|\ **p**\|\ **a**.

        **0**\ : Report range of z after actually scanning the data, not just
        reporting what the header says.
        **1**\ : Report median and L1 scale of z (L1 scale = 1.4826 * Median
        Absolute Deviation (MAD)).
        **2**\ : Report mean, standard deviation, and root-mean-square (rms)
        of z.
        **p**\ : Report mode (LMS) and LMS scale of z.
        **a**\ : Include all of the above.
    minxmax_pos : bool
        Include the x/y values at the location of the minimum and maximum
        z-values.
    nearest_multiple : str
        [*dz*]\ [**+a**\ [*alpha*]]\ [**+s**].
        Determine min and max z-value. If *dz* is provided then we first round
        these values off to multiples of *dz*. To exclude the two tails of the
        distribution when determining the min and max you can add **+a** to
        set the *alpha* value (in percent): We then sort the grid, exclude the
        data in the 0.5*\ *alpha* and 100 - 0.5*\ *alpha* tails, and revise
        the min and max. To force a symmetrical range about zero, using
        minus/plus the max absolute value of the two extremes, append **+s**\ .
        We report the result via the text string *zmin/zmax* or *zmin/zmax/dz*
        (if *dz* was given) as expected by :meth:`pygmt.makecpt`.
    {V}
    {f}

    Returns
    -------
    info : str
        A string with information about the grid.
    """
    with GMTTempFile() as outfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                arg_str = " ".join(
                    [infile, build_arg_string(kwargs), "->" + outfile.name]
                )
                lib.call_module("grdinfo", arg_str)
        result = outfile.read()
    return result
