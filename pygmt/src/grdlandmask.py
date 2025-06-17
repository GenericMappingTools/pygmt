"""
grdlandmask - Create a "wet-dry" mask grid from shoreline database.
"""

from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias
from pygmt.src._common import _parse_coastline_resolution

__doctest_skip__ = ["grdlandmask"]


@fmt_docstring
@use_alias(
    A="area_thresh",
    D="resolution-",
    E="bordervalues",
    I="spacing",
    N="maskvalues",
    R="region",
    V="verbose",
    r="registration",
    x="cores",
)
@kwargs_to_strings(I="sequence", R="sequence", N="sequence", E="sequence")
def grdlandmask(
    outgrid: PathLike | None = None,
    resolution: Literal[
        "auto", "full", "high", "intermediate", "low", "crude", None
    ] = None,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Create a "wet-dry" mask grid from shoreline database.

    Read the selected shoreline database and use that information to decide which nodes
    in the specified grid are over land or over water. The nodes defined by the selected
    region and lattice spacing will be set according to one of two criteria: (1) land vs
    water, or (2) the more detailed (hierarchical) ocean vs land vs lake vs island vs
    pond. A mask grid is created with the specified grid spacing.

    Full GMT docs at :gmt-docs:`grdlandmask.html`.

    {aliases}

    Parameters
    ----------
    {outgrid}
    {spacing}
    {region}
    {area_thresh}
    resolution
        Select the resolution of the coastline dataset to use. The available resolutions
        from highest to lowest are: ``"full"``, ``"high"``, ``"intermediate"``,
        ``"low"``, and ``"crude"``, which drops by 80% between levels. Alternatively,
        choose ``"auto"`` to automatically select the most suitable resolution given the
        chosen region. Note that because the coastlines differ in details, a node in a
        mask file using one resolution is not guaranteed to remain inside [or outside]
        when a different resolution is selected. If ``None``, the low resolution is used
        by default.
    maskvalues : list
        Set the values that will be assigned to nodes, in the form of [*wet*, *dry*], or
        [*ocean*, *land*, *lake*, *island*, *pond*]. Default is ``[0, 1, 0, 1, 0]``
        (i.e., ``[0, 1]``), meaning that all "wet" nodes will be assigned a value of 0
        and all "dry" nodes will be assigned a value of 1. Values can be any number, or
        one of ``None``, ``"NaN"``, and ``np.nan`` for setting nodes to NaN.

        Use ``bordervalues`` to control how nodes on feature boundaries are handled.
    bordervalues : bool, float, or list
        Sets the behavior for nodes that fall exactly on a polygon boundary. Valid
        values are:

        - ``False``: Treat boundary nodes as inside [Default]
        - ``True``: Treat boundary nodes as outside
        - A single value: Set all boundary nodes to the same value
        - A sequence of four values in the form of [*cborder*, *lborder*, *iborder*,
          *pborder*] to treat different kinds of boundary nodes as the specified values.
          *cborder* is for coastline, *lborder* for lake outline, *iborder* for
          islands-in-lakes outlines, and *pborder* for ponds-in-islands-in-lakes
          outlines.

        Values can be any number, or one of ``None``, ``"NaN"``, and ``np.nan`` for
        setting nodes to NaN.
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

    kwargs["D"] = kwargs.get("D", _parse_coastline_resolution(resolution))

    with Session() as lib:
        with lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd:
            kwargs["G"] = voutgrd
            lib.call_module(module="grdlandmask", args=build_arg_list(kwargs))
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
