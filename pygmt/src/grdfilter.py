"""
grdfilter - Filter a grid in the space (or time) domain.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias


@fmt_docstring
@use_alias(D="distance", F="filter", N="nans", f="coltypes")
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
    histogram_bin_width: float | None = None,
    histogram_center_bins: bool = False,
    mode_extreme: Literal["min", "max"] | None = None,
    toggle: bool = False,
    spacing: Sequence[float | str] | None = None,
    region: Sequence[float | str] | str | None = None,
    registration: Literal["gridline", "pixel"] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
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
       - I = spacing
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

    filter_type
      The filter type. Choose among convolution and non-convolution filters.

      Convolution filters are:

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

      Non-convolution filters are:

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
    median_quantile
        Quantile to use when ``filter_type="median"``. Must be a float in the range 0-1.
        [Default is 0.5 (median)].
    histogram_bin_width
        Bin width to use when ``filter_type="histogram"``.
    histogram_center_bins
        Center the histogram bins on multiples of *histogram_bin_width* when
        ``filter_type="histogram"``. By default, the bins are aligned such that
        their edges are on multiples of *histogram_bin_width*.
    mode_extreme
        Choose which extreme to return when ``filter_type="mlprob"`` and multiple modes
        are found. Options are: ``"min"`` to return the lowermost mode, or ``"max"`` to
        return the uppermost mode. By default, the average of all modes is returned.
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
    nans : str or float
        **i**\|\ **p**\|\ **r**.
        Determine how NaN-values in the input grid affect the filtered output.
        Use **i** to ignore all NaNs in the calculation of the filtered value
        [Default]. **r** is same as **i** except if the input node was NaN then
        the output node will be set to NaN (only applies if both grids are
        co-registered). **p** will force the filtered value to be NaN if any
        grid nodes with NaN-values are found inside the filter circle.
    $region
    toggle
        Toggle the node registration for the output grid so as to become the opposite of
        the input grid [Default gives the same registration as the input grid].
        Alternatively, use ``registration`` to set the registration explicitly.
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
    >>> # Apply a filter of 600 km (full width) to the @earth_relief_30m_g file
    >>> # and return a filtered field (saved as netCDF)
    >>> pygmt.grdfilter(
    ...     grid="@earth_relief_30m_g",
    ...     filter="m600",
    ...     distance="4",
    ...     region=[150, 250, 10, 40],
    ...     spacing=0.5,
    ...     outgrid="filtered_pacific.nc",
    ... )
    >>> Path("filtered_pacific.nc").unlink()  # Cleanup file
    >>> # Apply a Gaussian smoothing filter of 600 km to the input DataArray
    >>> # and return a filtered DataArray with the smoothed field
    >>> grid = pygmt.datasets.load_earth_relief()
    >>> smooth_field = pygmt.grdfilter(grid=grid, filter="g600", distance="4")
    """
    aliasdict = AliasSystem(
        F=[
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
            Alias(histogram_bin_width, name="histogram_bin_width", prefix="/"),
            Alias(highpass, name="highpass", prefix="+h"),
            Alias(median_quantile, name="median_quantile", prefix="+q"),
            Alias(histogram_center_bins, name="histogram_center_bins", prefix="+c"),
            Alias(
                mode_extreme, name="mode_extreme", mapping={"min": "+l", "max": "+u"}
            ),
        ],
        I=Alias(spacing, name="spacing", sep="/", size=2),
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
