"""
grdlandmask - Create a "wet-dry" mask grid from shoreline data base
"""
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray

__doctest_skip__ = ["grdlandmask"]


@fmt_docstring
@use_alias(
    A="area_thresh",
    D="resolution",
    E="bordervalues",
    G="outgrid",
    I="spacing",
    N="maskvalues",
    R="region",
    V="verbose",
    r="registration",
)
@kwargs_to_strings(I="sequence", R="sequence", N="sequence", E="sequence")
def grdlandmask(**kwargs):
    r"""
    Create a grid file with set values for land and water.

    Read the selected shoreline database and create a grid to specify which
    nodes in the specified grid are over land or over water. The nodes defined
    by the selected region and lattice spacing
    will be set according to one of two criteria: (1) land vs water, or
    (2) the more detailed (hierarchical) ocean vs land vs lake
    vs island vs pond.

    Full option list at :gmt-docs:`grdlandmask.html`

    {aliases}

    Parameters
    ----------
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {spacing}
    {region}
    {area_thresh}
    resolution : str
        *res*\[\ **+f**\]. Selects the resolution of the data set to use
        ((**f**)ull, (**h**)igh, (**i**)ntermediate, (**l**)ow, or
        (**c**)rude). The resolution drops off by ~80% between data sets.
        [Default is **l**]. Append **+f** to automatically select a lower
        resolution should the one requested not be available
        [abort if not found]. Alternatively, choose (**a**)uto to automatically
        select the best resolution given the chosen region. Note that because
        the coastlines differ in details a node in a mask file using one
        resolution is not guaranteed to remain inside [or outside] when a
        different resolution is selected.
    bordervalues : bool or str or float or list
        Nodes that fall exactly on a polygon boundary should be
        considered to be outside the polygon [Default considers them to be
        inside]. Alternatively, append either a list of four values
        [*cborder*, *lborder*, *iborder*, *pborder*] or just the single value
        *bordervalue* (for the case when they should all be the same value).
        This turns on the line-tracking mode. Now, after setting the mask
        values specified via ``maskvalues`` we trace the lines and change the
        node values for all cells traversed by a line to the corresponding
        border value. Here, *cborder* is used for cells traversed by the
        coastline, *lborder* for cells traversed by a lake outline, *iborder*
        for islands-in-lakes outlines, and *pborder* for
        ponds-in-islands-in-lakes outlines [Default is no line tracing].
    maskvalues : str or list
        [*wet*, *dry*] or [*ocean*, *land*, *lake*, *island*, *pond*].
        Sets the values that will be assigned to nodes. Values can
        be any number, including the textstring NaN
        [Default is [0, 1, 0, 1, 0] (i.e., [0, 1])]. Also select
        ``bordervalues`` to let nodes exactly on feature boundaries be
        considered outside [Default is inside].
    {verbose}
    {registration}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Create a landmask grid with an x-range of 125 to 130,
    >>> # and a y-range of 30 to 35
    >>> landmask = pygmt.grdlandmask(spacing=1, region=[125, 130, 30, 35])
    """
    if kwargs.get("I") is None or kwargs.get("R") is None:
        raise GMTInvalidInput("Both 'region' and 'spacing' must be specified.")

    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            if (outgrid := kwargs.get("G")) is None:
                kwargs["G"] = outgrid = tmpfile.name  # output to tmpfile
            lib.call_module(module="grdlandmask", args=build_arg_string(kwargs))

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
