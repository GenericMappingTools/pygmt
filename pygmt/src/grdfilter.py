"""
grdfilter - Filter a grid in the space (or time) domain.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias

__doctest_skip__ = ["grdfilter"]


@fmt_docstring
@use_alias(F="filter", f="coltypes")
def grdfilter(
    grid: PathLike | xr.DataArray,
    outgrid: PathLike | None = None,
    distance: Literal[
        "pixel",
        "cartesian",
        "geo_cartesian",
        "geo_flatearth1",
        "geo_flatearth2",
        "geo_spherical",
        "geo_mercator",
    ]
    | None = None,
    spacing: Sequence[float | str] | None = None,
    nans: Literal["ignore", "replace", "preserve"] | None = None,
    toggle: bool = False,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    registration: Literal["gridline", "pixel"] | bool = False,
    cores: int | bool = False,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Filter a grid in the space (or time) domain.

    Filter a grid file in the space (or time) domain using one of the selected
    convolution or non-convolution isotropic or rectangular filters and compute
    distances using Cartesian or Spherical geometries. The output grid file
    can optionally be generated as a sub-region of the input (via ``region``)
    and/or with new increment (via ``spacing``) or registration
    (via ``toggle``). In this way, one may have "extra space" in the input
    data so that the edges will not be used and the output can be within one
    half-width of the input edges. If the filter is low-pass, then the output
    may be less frequently sampled than the input.

    Full GMT docs at :gmt-docs:`grdfilter.html`.

    $aliases
       - D = distance
       - G = outgrid
       - I = spacing
       - N = nans
       - R = region
       - T = toggle
       - V = verbose
       - r = registration
       - x = cores

    Parameters
    ----------
    $grid
    $outgrid
    filter : str
        **b**\|\ **c**\|\ **g**\|\ **o**\|\ **m**\|\ **p**\|\ **h**\ *width*\
        [/*width2*\][*modifiers*].
        Name of the filter type you wish to apply, followed by the *width*:

        - **b**: Box Car
        - **c**: Cosine Arch
        - **g**: Gaussian
        - **o**: Operator
        - **m**: Median
        - **p**: Maximum Likelihood probability
        - **h**: Histogram

    distance
        Determine how grid (*x, y*) relates to filter *width* and how distances are
        calculated. Valid values are list below. The first four options are fastest
        because they allow weight matrix to be computed only once. The last three
        options are slower because they recompute weights for each latitude.

        .. list-table::
            :header-rows: 1
            :widths: 16 32 20 32

            * - Value
              - Grid (x,y)
              - Width
              - Distance Calculation
            * - ``"pixel"``
              - Pixels (px, py)
              - Odd number of pixels
              - Cartesian
            * - ``"cartesian"``
              - Same units as *width*
              - Any
              - Cartesian
            * - ``"geo_cartesian"``
              - Degrees
              - km
              - Cartesian
            * - ``"geo_flatearth1"``
              - Degrees
              - km
              - Cartesian, dx scaled by cos(middle y)
            * - ``"geo_flatearth2"``
              - Degrees
              - km
              - Cartesian, dx scaled by cos(y) per row
            * - ``"geo_spherical"``
              - Degrees
              - km
              - Spherical (great circle)
            * - ``"geo_mercator"``
              - Mercator **-Jm1** img units
              - km
              - Spherical
    $spacing
    nans
        Determine how NaN-values in the input grid affect the filtered output grid.
        Choose one of:

        - ``"ignore"``: Ignore all NaNs in the calculation of filtered value [Default].
        - ``"replace"``: Similar to ``"ignore"`` except if the input node was NaN then
          the output node will be set to NaN (only applied if both grids are
          co-registered).
        - ``"preserve"``: Force the filtered value to be NaN if any grid nodes with
          NaN-values are found inside the filter circle.
    toggle
        Toggle the node registration for the output grid so as to become the opposite of
        the input grid [Default gives the same registration as the input grid].
        Alternatively, use ``registration`` to set the registration explicitly.
    $region
    $verbose
    $coltypes
    $registration
    $cores

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - ``None`` if ``outgrid`` is set (grid output will be stored in the file set by
          ``outgrid``)

    Examples
    --------
    >>> from pathlib import Path
    >>> import pygmt
    >>> # Apply a median filter of 600 km (full width) to the @earth_relief_30m_g grid
    >>> # and return a filtered grid (saved as netCDF file).
    >>> pygmt.grdfilter(
    ...     grid="@earth_relief_30m_g",
    ...     filter="m600",
    ...     distance="geo_spherical",
    ...     region=[150, 250, 10, 40],
    ...     spacing=0.5,
    ...     outgrid="filtered_pacific.nc",
    ... )
    >>> Path("filtered_pacific.nc").unlink()  # Cleanup file
    >>> # Apply a Gaussian smoothing filter of 600 km to the input DataArray and return
    >>> # a filtered DataArray with the smoothed grid.
    >>> grid = pygmt.datasets.load_earth_relief()
    >>> smoothed = pygmt.grdfilter(grid=grid, filter="g600", distance="geo_spherical")
    """
    if kwargs.get("D", distance) is None:
        raise GMTParameterError(required="distance")

    aliasdict = AliasSystem(
        D=Alias(
            distance,
            name="distance",
            mapping={
                "pixel": "p",
                "cartesian": 0,
                "geo_cartesian": 1,
                "geo_flatearth1": 2,
                "geo_flatearth2": 3,
                "geo_spherical": 4,
                "geo_mercator": 5,
            },
        ),
        I=Alias(spacing, name="spacing", sep="/", size=2),
        N=Alias(
            nans, name="nans", mapping={"ignore": "i", "replace": "r", "preserve": "p"}
        ),
        T=Alias(toggle, name="toggle"),
    ).add_common(
        R=region,
        V=verbose,
        r=registration,
        x=cores,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            aliasdict["G"] = voutgrd
            lib.call_module(
                module="grdfilter", args=build_arg_list(aliasdict, infile=vingrd)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
