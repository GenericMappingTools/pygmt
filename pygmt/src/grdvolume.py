"""
grdvolume - Calculate grid volume and area constrained by a contour.
"""

from typing import Literal

import numpy as np
import pandas as pd
from pygmt.clib import Session
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
    validate_output_table_type,
)

__doctest_skip__ = ["grdvolume"]


@fmt_docstring
@use_alias(
    C="contour",
    R="region",
    S="unit",
    V="verbose",
)
@kwargs_to_strings(C="sequence", R="sequence")
def grdvolume(
    grid,
    output_type: Literal["pandas", "numpy", "file"] = "pandas",
    outfile: str | None = None,
    **kwargs,
) -> pd.DataFrame | np.ndarray | None:
    r"""
    Determine the volume between the surface of a grid and a plane.

    Read a 2-D grid file and calculate the volume contained below the surface
    and above the plane specified by the given contour (or zero if not given)
    and return the contour, area, volume, and maximum mean height
    (volume/area). Alternatively, a range of contours can be specified to
    return the volume and area inside the contour for all contour values.

    Full option list at :gmt-docs:`grdvolume.html`

    {aliases}

    Parameters
    ----------
    {grid}
    {output_type}
    {outfile}
    contour : str, float, or list
        *cval*\|\ *low/high/delta*\|\ **r**\ *low/high*\|\ **r**\ *cval*.
        Find area, volume and mean height (volume/area) inside and above the
        *cval* contour. Alternatively, search using all contours from *low* to
        *high* in steps of *delta*. [Default returns area, volume and mean
        height of the entire grid]. The area is measured in the plane of the
        contour. Adding the **r** prefix computes the volume below the grid
        surface and above the planes defined by *low* and *high*, or below
        *cval* and  grid's minimum. Note that this is an *outside* volume
        whilst the other forms compute an *inside* (below the surface) area
        volume. Use this form to compute for example the volume of water
        between two contours. If no *contour* is given then there is no contour
        and the entire grid area, volume and the mean height is returned and
        *cval* will be reported as 0.
    {region}
    {verbose}

    Returns
    -------
    ret
        Return type depends on ``outfile`` and ``output_type``:

        - ``None`` if ``outfile`` is set (output will be stored in file set by
          ``outfile``)
        - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if ``outfile`` is not set
          (depends on ``output_type``)

    Example
    -------
    >>> import pygmt
    >>> # Load a grid of @earth_relief_30m data, with a longitude range of
    >>> # 10° E to 30° E, and a latitude range of 15° N to 25° N
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 30, 15, 25]
    ... )
    >>> # Create a pandas dataframe that contains the contour, area, volume,
    >>> # and maximum mean height above the plane specified by the given
    >>> # contour and below the surface; set the minimum contour z-value to
    >>> # 200, the maximum to 400, and the interval to 50.
    >>> output_dataframe = pygmt.grdvolume(
    ...     grid=grid, contour=[200, 400, 50], output_type="pandas"
    ... )
    >>> print(output_dataframe)
           0             1             2           3
    0  200.0  2.323600e+12  8.523815e+14  366.836554
    1  250.0  2.275864e+12  7.371655e+14  323.905736
    2  300.0  2.166707e+12  6.258570e+14  288.851699
    3  350.0  2.019284e+12  5.207732e+14  257.899955
    4  400.0  1.870441e+12  4.236191e+14  226.480847
    """
    output_type = validate_output_table_type(output_type, outfile=outfile)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="dataset", fname=outfile) as vouttbl,
        ):
            lib.call_module(
                module="grdvolume",
                args=build_arg_list(kwargs, infile=vingrd, outfile=vouttbl),
            )
            return lib.virtualfile_to_dataset(vfname=vouttbl, output_type=output_type)
