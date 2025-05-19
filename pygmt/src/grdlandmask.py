"""
grdlandmask - Create a "wet-dry" mask grid from shoreline database.
"""

from collections.abc import Sequence

import numpy as np
import xarray as xr
from pygmt._typing import PathLike
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["grdlandmask"]


def _parse_maskvalues(maskvalues: Sequence[str, float, None] | None) -> str | None:
    """
    Parse the argument for the ``maskvalues`` parameter.

    Examples
    --------
    >>> _parse_maskvalues([0, 1])
    '0/1'
    >>> _parse_maskvalues([0, 1, 0, 1, 0])
    '0/1/0/1/0'
    >>> _parse_maskvalues([0, 1, None, 1, 0])
    '0/1/NaN/1/0'
    >>> _parse_maskvalues([0, 1, np.nan, 1, 0])
    '0/1/NaN/1/0'
    >>> _parse_maskvalues([0, 1, "NaN", 1, 0])
    '0/1/NaN/1/0'
    >>> _parse_maskvalues([0, 1, "NaN", 1, 0])
    '0/1/NaN/1/0'

    >>> _parse_maskvalues([0, 1, 2])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: "'maskvalues' must be a sequence of 2 or ..."
    """
    if maskvalues is None:
        return None

    if len(maskvalues) not in {2, 5}:
        msg = "'maskvalues' must be a sequence of 2 or 5 values."
        raise GMTInvalidInput(msg)

    return "/".join(
        [
            "NaN" if x is None or (isinstance(x, float) and np.isnan(x)) else x
            for x in maskvalues
        ]
    )


@fmt_docstring
@use_alias(
    A="area_thresh",
    D="resolution",
    E="bordervalues",
    I="spacing",
    R="region",
    V="verbose",
    r="registration",
    x="cores",
)
@kwargs_to_strings(I="sequence", R="sequence", E="sequence")
def grdlandmask(
    outgrid: PathLike | None = None,
    maskvalues: Sequence[str, float, None] | None = None,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Create a "wet-dry" mask grid from shoreline database.

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
    {outgrid}
    {spacing}
    {region}
    {area_thresh}
    resolution : str
        *res*\[\ **+f**\]. Select the resolution of the data set to use
        ((**f**)ull, (**h**)igh, (**i**)ntermediate, (**l**)ow, or
        (**c**)rude). The resolution drops off by ~80% between data sets.
        [Default is **l**]. Append **+f** to automatically select a lower
        resolution should the one requested not be available
        [abort if not found]. Alternatively, choose (**a**)uto to automatically
        select the best resolution given the chosen region. Note that because
        the coastlines differ in details a node in a mask file using one
        resolution is not guaranteed to remain inside [or outside] when a
        different resolution is selected.
    bordervalues : bool, str, float, or list
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
        Set the values that will be assigned to nodes. Values can
        be any number, including the textstring NaN
        [Default is [0, 1, 0, 1, 0] (i.e., [0, 1])]. Also select
        ``bordervalues`` to let nodes exactly on feature boundaries be
        considered outside [Default is inside].
    {verbose}
    {registration}
    {cores}

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - ``None`` if ``outgrid`` is set (grid output will be stored in the file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Create a landmask grid with a longitude range of 125° E to 130° E, a
    >>> # latitude range of 30° N to 35° N, and a grid spacing of 1 arc-degree
    >>> landmask = pygmt.grdlandmask(spacing=1, region=[125, 130, 30, 35])
    """
    if kwargs.get("I") is None or kwargs.get("R") is None:
        msg = "Both 'region' and 'spacing' must be specified."
        raise GMTInvalidInput(msg)

    if maskvalues is not None:
        kwargs["N"] = _parse_maskvalues(maskvalues)

    with Session() as lib:
        with lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd:
            kwargs["G"] = voutgrd
            lib.call_module(module="grdlandmask", args=build_arg_list(kwargs))
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
