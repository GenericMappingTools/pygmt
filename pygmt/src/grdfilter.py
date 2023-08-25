"""
grdfilter - Filter a grid in the space (or time) domain.
"""

from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray


@fmt_docstring
@use_alias(
    D="distance",
    F="filter",
    G="outgrid",
    I="spacing",
    N="nans",
    R="region",
    T="toggle",
    V="verbose",
    f="coltypes",
    r="registration",
    x="cores",
)
@kwargs_to_strings(I="sequence", R="sequence")
def grdfilter(grid, **kwargs):
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

    Full option list at :gmt-docs:`grdfilter.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a
        :class:`xarray.DataArray`.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    filter : str
        **b**\|\ **c**\|\ **g**\|\ **o**\|\ **m**\|\ **p**\|\ **h**\ *width*\
        [/*width2*\][*modifiers*].
        Name of the filter type you wish to apply, followed by the *width*:

        - **b** - Box Car
        - **c** - Cosine Arch
        - **g** - Gaussian
        - **o** - Operator
        - **m** - Median
        - **p** - Maximum Likelihood probability
        - **h** - Histogram

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

    {spacing}
    nans : str or float
        **i**\|\ **p**\|\ **r**.
        Determine how NaN-values in the input grid affect the filtered output.
        Use **i** to ignore all NaNs in the calculation of the filtered value
        [Default]. **r** is same as **i** except if the input node was NaN then
        the output node will be set to NaN (only applies if both grids are
        co-registered). **p** will force the filtered value to be NaN if any
        grid nodes with NaN-values are found inside the filter circle.
    {region}
    toggle : bool
        Toggle the node registration for the output grid to get the opposite of
        the input grid [Default gives the same registration as the input grid].
    {verbose}
    {coltypes}
    {registration}
    {cores}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Examples
    --------
    >>> import os
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
    >>> os.remove("filtered_pacific.nc")  # Cleanup file
    >>> # Apply a Gaussian smoothing filter of 600 km to the input DataArray
    >>> # and return a filtered DataArray with the smoothed field
    >>> grid = pygmt.datasets.load_earth_relief()
    >>> smooth_field = pygmt.grdfilter(grid=grid, filter="g600", distance="4")
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if (outgrid := kwargs.get("G")) is None:
                    kwargs["G"] = outgrid = tmpfile.name  # output to tmpfile
                lib.call_module(
                    module="grdfilter", args=build_arg_string(kwargs, infile=infile)
                )

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
