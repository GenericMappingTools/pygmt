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
    filter_type=None,
    filter_width=None,
    hist_bin_width=None,
    highpass=False,
    median_quantile=None,
    hist_center_bins=False,
    mode_extreme=None,
    filter=None,  # noqa: A002
):
    """
    Helper function to create the alias list for the -F option.

    Examples
    --------
    >>> def parse(**kwargs):
    ...     return AliasSystem(F=_alias_option_F(**kwargs)).get("F")
    >>> parse(filter_type="boxcar", filter_width=2.0)
    'b2.0'
    >>> parse(filter_type="cosine_arch", filter_width=(5, 10))
    'c5/10'
    >>> parse(filter_type="gaussian", filter_width=100, highpass=True)
    'g100+h'
    >>> parse(filter_type="median", median_quantile=0.25)
    'm+q0.25'
    >>> parse(
    ...     filter_type="histogram",
    ...     filter_width=100,
    ...     hist_bin_width=1.0,
    ...     hist_center_bins=True,
    ...     mode_extreme="max",
    ... )
    'h100/1.0+c+u'
    """
    if filter is not None:
        kwdict = {
            "filter_type": filter_type,
            "filter_width": filter_width,
            "hist_bin_width": hist_bin_width,
            "highpass": highpass,
            "median_quantile": median_quantile,
            "hist_center_bins": hist_center_bins,
            "mode_extreme": mode_extreme,
        }
        if any(v is not None and v is not False for v in kwdict.values()):
            raise GMTParameterError(
                conflicts_with=("filter", kwdict.keys()),
                reason="'filter' is specified using the unrecommended GMT command string syntax.",
            )
        return Alias(filter, name="filter")  # Deprecated raw GMT string.

    if median_quantile is not None and filter_type != "median":
        raise GMTParameterError(
            conflicts_with=("median_quantile", [f"filter_type={filter_type!r}"]),
            reason="'median_quantile' is allowed only when 'filter_type' is 'median'.",
        )
    if hist_bin_width is not None and filter_type != "histogram":
        raise GMTParameterError(
            conflicts_with=("hist_bin_width", [f"filter_type={filter_type!r}"]),
            reason="'hist_bin_width' is allowed only when 'filter_type' is 'histogram'.",
        )
    if hist_center_bins is not False and filter_type != "histogram":
        raise GMTParameterError(
            conflicts_with=("hist_center_bins", [f"filter_type={filter_type!r}"]),
            reason="'hist_center_bins' is allowed only when 'filter_type' is 'histogram'.",
        )
    if mode_extreme is not None and filter_type not in {"mlprob", "histogram"}:
        raise GMTParameterError(
            conflicts_with=("mode_extreme", [f"filter_type={filter_type!r}"]),
            reason="'mode_extreme' is allowed only when 'filter_type' is 'mlprob' or 'histogram'.",
        )

    return [
        Alias(
            filter_type,
            name="filter_type",
            mapping={
                "boxcar": "b",
                "cosine_arch": "c",
                "gaussian": "g",
                "custom": "f",
                "operator": "o",
                "median": "m",
                "mlprob": "p",
                "histogram": "h",
                "minall": "l",
                "minpos": "L",
                "maxall": "u",
                "maxneg": "U",
            },
        ),
        Alias(filter_width, name="filter_width", sep="/"),
        Alias(hist_bin_width, name="hist_bin_width", prefix="/"),
        Alias(hist_center_bins, name="hist_center_bins", prefix="+c"),
        Alias(highpass, name="highpass", prefix="+h"),
        Alias(median_quantile, name="median_quantile", prefix="+q"),
        Alias(mode_extreme, name="mode_extreme", mapping={"min": "+l", "max": "+u"}),
    ]


@fmt_docstring
@use_alias(D="distance", f="coltypes")
def grdfilter(  # noqa: PLR0913
    grid: PathLike | xr.DataArray,
    outgrid: PathLike | None = None,
    filter_type: Literal[
        "boxcar",
        "cosine_arch",
        "gaussian",
        "custom",
        "operator",
        "median",
        "mlprob",
        "histogram",
        "minall",
        "minpos",
        "maxall",
        "maxneg",
    ]
    | None = None,
    filter_width: Sequence[float] | None = None,
    highpass: bool = False,
    median_quantile: float | None = None,
    hist_bin_width: float | None = None,
    hist_center_bins: bool = False,
    mode_extreme: Literal["min", "max"] | None = None,
    filter: str | None = None,  # noqa: A002
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
    filter_type
      The filter type. Choose among convolution and non-convolution filters.

      Convolution filters include:

      - ``"boxcar"``: All weights are equal.
      - ``"cosine_arch"``: Weights follow a cosine arch curve.
      - ``"gaussian"``: Weights are given by the Gaussian function, where filter width
        is 6 times the conventional Gaussian sigma.
      - ``"custom"``: Weights are given by the precomputed values in the filter weight
        grid file *weight*, which must have odd dimensions; also requires ``distance=0``
        and output spacing must match input spacing or be integer multiples.
      - ``"operator"``: Weights are given by the precomputed values in the filter weight
        grid file *weight*, which must have odd dimensions; also requires ``distance=0``
        and output spacing must match input spacing or be integer multiples. Weights
        are assumed to sum to zero so no accumulation of weight sums and normalization
        will be done.

      Non-convolution filters include:

      - ``"median"``: Returns median value. To select another quantile, use the
        parameter ``median_quantile`` in the 0-1 range [Default is 0.5, i.e., median].
      - ``"mlprob"``: Maximum likelihood probability (a mode estimator). Return modal
        value. If more than one mode is found we return their average value. Set
        ``mode_extreme`` to ``"min"`` or ``"max"`` to return the lowermost or uppermost
        of the modal values.
      - ``"histogram"``: Histogram mode (another mode estimator). Return the modal value
        as the center of the dominant peak in a histogram. Use parameter
        ``histogram_center_bins`` to center the bins on multiples of bin width [Default
        has bin edges that are multiples of bin width]. Use parameter
        ``histogram_bin_width`` to set the bin width. If more than one mode is found we
        return their average value. Set ``mode_extreme`` to ``"min"`` or ``"max"`` to
        return the lowermost or uppermost of the modal values.

      - ``"minall"``: Return minimum of all values.
      - ``"minpos"``: Return minimum of all positive values only.
      - ``"maxall"``: Return maximum of all values.
      - ``"maxneg"``: Return maximum of all negative values only.
    filter_width
        The full diameter width of the filter. It can be a single value for an isotropic
        filter, or a pair of values for a rectangular filter (width in x- and
        y-directions, requiring ``distance`` be either ``"p"`` or ``0``). For isotropic
        filters, ``width`` can also be a path to a grid file for variable filter width,
        in which case the grid must have the same registration and dimensions as the
        output filtered grid.
    highpass
        By default, the filter is a low-pass filter. If True, then the filter is a
        high-pass filter. [Default is ``False``].
    median_quantile
        Quantile to use when ``filter_type="median"``. Must be a float in the range 0-1.
        [Default is 0.5 (median)].
    hist_bin_width
        Bin width to use when ``filter_type="histogram"``.
    hist_center_bins
        Center the histogram bins on multiples of *histogram_bin_width* when
        ``filter_type="histogram"``. By default, the bins are aligned such that
        their edges are on multiples of *hist_bin_width*.
    mode_extreme
        Choose which extreme to return when ``filter_type="mlprob"`` or
        ``filter_type="histogram"`` and multiple modes are found. Options are: ``"min"``
        to return the lowermost mode, or ``"max"`` to return the uppermost mode. By
        default, the average of all modes is returned.
    filter
        Set the filter type.

        .. deprecated:: v0.19.0

            This parameter is deprecated. Use the parameters ``filter_type``,
            ``filter_width``, ``hist_bin_width``, ``highpass``, ``median_quantile``,
            ``hist_center_bins``, and ``mode_extreme`` instead. This parameter still
            accepts raw GMT CLI strings for the ``-F`` option of the ``grdfilter``
            module for backward compatibility.
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
    ...     filter_type="median",
    ...     filter_width=600,
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
    ...     grid=grid, filter_type="gaussian", filter_width=600, distance="4"
    ... )
    """
    aliasdict = AliasSystem(
        F=_alias_option_F(
            filter_type=filter_type,
            filter_width=filter_width,
            hist_bin_width=hist_bin_width,
            highpass=highpass,
            median_quantile=median_quantile,
            hist_center_bins=hist_center_bins,
            mode_extreme=mode_extreme,
            filter=filter,
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
