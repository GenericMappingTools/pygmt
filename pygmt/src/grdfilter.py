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


def _alias_option_F(  # noqa: N802
    filter=None,  # noqa: A002
    width=None,
    highpass=False,
):
    """
    Helper function to create the alias list for the -F option.

    Examples
    --------
    >>> def parse(**kwargs):
    ...     return AliasSystem(F=_alias_option_F(**kwargs)).get("F")
    >>> parse(filter="boxcar", width=2.0)
    'b2.0'
    >>> parse(filter="cosarch", width=(5, 10))
    'c5/10'
    >>> parse(filter="gaussian", width=100, highpass=True)
    'g100+h'
    """
    _filter_mapping = {
        "boxcar": "b",
        "cosarch": "c",
        "gaussian": "g",
        "minall": "l",
        "minpos": "L",
        "maxall": "u",
        "maxneg": "U",
    }
    # Check if the 'filter' parameter is using the old GMT command string syntax.
    _old_filter_syntax = isinstance(filter, str) and filter not in _filter_mapping

    if _old_filter_syntax:
        kwdict = {"width": width, "highpass": highpass}
        if any(v is not None and v is not False for v in kwdict.values()):
            raise GMTParameterError(
                conflicts_with=("filter", kwdict.keys()),
                reason="'filter' is specified using the unrecommended GMT command string syntax.",
            )
        return Alias(filter, name="filter")  # Deprecated raw GMT command string.

    if filter is None or width is None:
        raise GMTParameterError(required=["filter", "width"])

    return [
        Alias(filter, name="filter", mapping=_filter_mapping),
        Alias(width, name="width", sep="/", size=2),
        Alias(highpass, name="highpass", prefix="+h"),
    ]


@fmt_docstring
@use_alias(D="distance", f="coltypes")
def grdfilter(  # noqa: PLR0913
    grid: PathLike | xr.DataArray,
    outgrid: PathLike | None = None,
    filter: Literal[  # noqa: A002
        "boxcar", "cosarch", "gaussian", "minall", "minpos", "maxall", "maxneg"
    ]
    | str
    | None = None,
    width: float | Sequence[float] | None = None,
    highpass: bool = False,
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
    """
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
       - F = filter, width, **+h**: highpass
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
    filter
      The filter type. Choose among convolution and non-convolution filters.

      Convolution filters include:

      - ``"boxcar"``: All weights are equal.
      - ``"cosarch"``: Weights follow a cosine arch curve.
      - ``"gaussian"``: Weights are given by the Gaussian function, where filter width
        is 6 times the conventional Gaussian sigma.

      Non-convolution filters include:

      - ``"minall"``: Return minimum of all values.
      - ``"minpos"``: Return minimum of all positive values only.
      - ``"maxall"``: Return maximum of all values.
      - ``"maxneg"``: Return maximum of all negative values only.

      **Note**: There are still a few other filter types available in GMT (e.g.,
      histogram and mode filters), but they are not implemented in PyGMT yet. As a
      workaround, pass the raw GMT command string to this parameter to use these other
      filter types. Refer to :gmt-docs:`grdfilter.html#f` for the full syntax of this
      parameter.
    width
        The full diameter width of the filter. It can be a single value for an isotropic
        filter, or a pair of values for a rectangular filter (width in x- and
        y-directions, requiring ``distance`` be either ``"p"`` or ``0``).
    highpass
        By default, the filter is a low-pass filter. If True, then the filter is a
        high-pass filter. [Default is ``False``].
    distance : str
        State how the grid (x,y) relates to the filter *width*:

        - ``"p"``: grid (px,py) with *width* an odd number of pixels,
          Cartesian distances.
        - ``"0"``: grid (x,y) same units as *width*, Cartesian distances.
        - ``"1"``: grid (x,y) in degrees, *width* in kilometers, Cartesian
          distances.
        - ``"2"``: grid (x,y) in degrees, *width* in km, dx scaled by
          cos(middle y), Cartesian distances.

        The above options are fastest because they allow weight matrix to be
        computed only once. The next three options are slower because they
        recompute weights for each latitude.

        - ``"3"``: grid (x,y) in degrees, *width* in km, dx scaled by cos(y),
          Cartesian distance calculation.
        - ``"4"``: grid (x,y) in degrees, *width* in km, Spherical distance
          calculation.
        - ``"5"``: grid (x,y) in Mercator ``projection="m1"`` img units,
          *width* in km, Spherical distance calculation.
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
    ...     filter="gaussian",
    ...     width=600,
    ...     distance="4",
    ...     region=[150, 250, 10, 40],
    ...     spacing=0.5,
    ...     outgrid="filtered_pacific.nc",
    ... )
    >>> Path("filtered_pacific.nc").unlink()  # Cleanup file
    >>> # Apply a Gaussian smoothing filter of 600 km to the input DataArray and return
    >>> # a filtered DataArray with the smoothed grid.
    >>> grid = pygmt.datasets.load_earth_relief()
    >>> smooth_field = pygmt.grdfilter(
    ...     grid=grid, filter="gaussian", width=600, distance="4"
    ... )
    """
    if kwargs.get("F", filter) is None:
        raise GMTParameterError(required="filter")

    aliasdict = AliasSystem(
        F=_alias_option_F(
            filter=filter,
            width=width,
            highpass=highpass,
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
