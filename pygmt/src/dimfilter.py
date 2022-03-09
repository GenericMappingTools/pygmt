"""
dimfilter - Directional filtering of grids in the space domain.
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


@fmt_docstring
@use_alias(
    D="distance",
    F="filter",
    G="outgrid",
    I="spacing",
    N="sectors",
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def dimfilter(grid, **kwargs):
    r"""
    Filter a grid by dividing the filter circle.

    Filter a grid in the space (or time) domain by
    dividing the given filter circle into the given number of sectors,
    applying one of the selected primary convolution or non-convolution
    filters to each sector, and choosing the final outcome according to the
    selected secondary filter. It computes distances using Cartesian or
    Spherical geometries. The output grid can optionally be generated as a
    subregion of the input and/or with a new increment using ``spacing``,
    which may add an "extra space" in the input data to prevent edge
    effects for the output grid. If the filter is low-pass, then the output
    may be less frequently sampled than the input. **dimfilter** will not
    produce a smooth output as other spatial filters
    do because it returns a minimum median out of *N* medians of *N*
    sectors. The output can be rough unless the input data is noise-free.
    Thus, an additional filtering (e.g., Gaussian via :func:`pygmt.grdfilter`)
    of the DiM-filtered data is generally recommended.

    Full option list at :gmt-docs:`dimfilter.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    distance : int or str
        Distance flag tells how grid (x,y) relates to filter width, as follows:

        - **0**\ : grid (x,y) in same units as *width*, Cartesian distances.
        - **1**\ : grid (x,y) in degrees, *width* in kilometers, Cartesian
          distances.
        - **2**\ : grid (x,y) in degrees, *width* in km, dx scaled by
          cos(middle y), Cartesian distances.

        The above options are fastest because they allow weight matrix to be
        computed only once. The next two options are slower because they
        recompute weights for each latitude.

        - **3**\ : grid (x,y) in degrees, *width* in km, dx scaled by
          cosine(y), Cartesian distance calculation.
        - **4**\ : grid (x,y) in degrees, *width* in km, Spherical distance
          calculation.
    filter : str
        **x**\ *width*\ [**+l**\|\ **u**]
        Sets the primary filter type. Choose among convolution and
        non-convolution filters. Append the filter code **x** followed by
        the full diameter *width*. Available convolution filters are:

        - (**b**) Boxcar: All weights are equal.
        - (**c**) Cosine Arch: Weights follow a cosine arch curve.
        - (**g**) Gaussian: Weights are given by the Gaussian function.

        Non-convolution filters are:

        - (**m**) Median: Returns median value.
        - (**p**) Maximum likelihood probability (a mode estimator): Return
          modal value. If more than one mode is found we return their average
          value. Append **+l** or **+h** to the filter width if you want
          to return the smallest or largest of each sector's modal values.
    sectors : str
        **x**\ *sectors*\ [**+l**\|\ **u**]
        Sets the secondary filter type **x** and the number of bow-tie sectors.
        *sectors* must be integer and larger than 0. When *sectors* is
        set to 1, the secondary filter is not effective. Available secondary
        filters **x** are:

        - (**l**) Lower: Return the minimum of all filtered values.
        - (**u**) Upper: Return the maximum of all filtered values.
        - (**a**) Average: Return the mean of all filtered values.
        - (**m**) Median: Return the median of all filtered values.
        - (**p**) Mode: Return the mode of all filtered values:
          If more than one mode is found we return their average
          value. Append **+l** or **+h** to the sectors if you rather want to
          return the smallest or largest of the modal values.
    spacing : str
        *x_inc* [and optionally *y_inc*] is the output Increment. Append
        **m** to indicate minutes, or **c** to indicate seconds. If the new
        *x_inc*, *y_inc* are NOT integer multiples of the old ones (in the
        input data), filtering will be considerably slower. [Default: Same
        as input.]
    region : str or list
        [*xmin*, *xmax*, *ymin*, *ymax*].
        Defines the region of the output points. [Default: Same as input.]
    {V}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    if ("D" not in kwargs) or ("F" not in kwargs) or ("N" not in kwargs):
        raise GMTInvalidInput(
            """At least one of the following parameters must be specified:
            distance, filters, or sectors."""
        )

    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if "G" not in kwargs:  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("dimfilter", arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
