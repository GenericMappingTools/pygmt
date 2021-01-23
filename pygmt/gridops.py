"""
GMT modules for grid operations.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    G="outgrid",
    R="region",
    J="projection",
    N="extend",
    S="circ_subregion",
    V="verbose",
    Z="z_subregion",
)
@kwargs_to_strings(R="sequence")
def grdcut(grid, **kwargs):
    """
    Extract subregion from a grid.

    Produce a new *outgrid* file which is a subregion of *grid*. The
    subregion is specified with *region*; the specified range must not exceed
    the range of *grid* (but see *extend*). If in doubt, run
    :meth:`pygmt.grdinfo` to check range. Alternatively, define the subregion
    indirectly via a range check on the node values or via distances from a
    given point. Finally, you can give *projection* for oblique projections to
    determine the corresponding rectangular *region* setting that will give a
    grid that fully covers the oblique domain.

    Full option list at :gmt-docs:`grdcut.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {J}
    {R}
    extend : bool or int or float
        Allow grid to be extended if new *region* exceeds existing boundaries.
        Give a value to initialize nodes outside current region.
    circ_subregion : str
        ``'lon/lat/radius[unit][+n]'``.
        Specify an origin (*lon* and *lat*) and *radius*; append a distance
        *unit* and we determine the corresponding rectangular region so that
        all grid nodes on or inside the circle are contained in the subset.
        If **+n** is appended we set all nodes outside the circle to NaN.
    z_subregion : str
        ``'[min/max][+n|N|r]'``.
        Determine a new rectangular region so that all nodes outside this
        region are also outside the given z-range [-inf/+inf]. To indicate no
        limit on *min* or *max* only, specify a hyphen (-). Normally, any NaNs
        encountered are simply skipped and not considered in the
        range-decision. Append **+n** to consider a NaN to be outside the given
        z-range. This means the new subset will be NaN-free. Alternatively,
        append **+r** to consider NaNs to be within the data range. In this
        case we stop shrinking the boundaries once a NaN is found [Default
        simply skips NaNs when making the range decision]. Finally, if your
        core subset grid is surrounded by rows and/or columns that are all
        NaNs, append **+N** to strip off such columns before (optionally)
        considering the range of the core subset for further reduction of the
        area.

    {V}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the *outgrid* parameter is set:

        - xarray.DataArray if *outgrid* is not set
        - None if *outgrid* is set (grid output will be stored in *outgrid*)
    """
    kind = data_kind(grid)

    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            if kind == "file":
                file_context = dummy_context(grid)
            elif kind == "grid":
                file_context = lib.virtualfile_from_grid(grid)
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(grid)))

            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdcut", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            with xr.open_dataarray(outgrid) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        else:
            result = None  # if user sets an outgrid, return None

        return result


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
)
@kwargs_to_strings(R="sequence")
def grdfilter(grid, **kwargs):
    """
    Filter a grid in the space (or time) domain.

    Filter a grid file in the time domain using one of the selected convolution
    or non-convolution isotropic or rectangular filters and compute distances
    using Cartesian or Spherical geometries. The output grid file can
    optionally be generated as a sub-region of the input (via *region*) and/or
    with new increment (via *spacing*) or registration (via *toggle*). In this
    way, one may have "extra space" in the input data so that the edges will
    not be used and the output can be within one half-width of the input edges.
    If the filter is low-pass, then the output may be less frequently sampled
    than the input.

    Full option list at :gmt-docs:`grdfilter.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    filter : str
        ``xwidth[/width2][modifiers]``.
        Name of filter type you which to apply, followed by the width
        b: Box Car; c: Cosine Arch; g: Gaussian; o: Operator; m: Median;
        p: Maximum Likelihood probability; h: histogram
        Example: F='m600' for a median filter with width of 600
    distance : str
        Distance *flag* tells how grid (x,y) relates to filter width as
        follows:

        p: grid (px,py) with *width* an odd number of pixels; Cartesian
        distances.

        0: grid (x,y) same units as *width*, Cartesian distances.

        1: grid (x,y) in degrees, *width* in kilometers, Cartesian distances.

        2: grid (x,y) in degrees, *width* in km, dx scaled by cos(middle y),
        Cartesian distances.

        The above options are fastest because they allow weight matrix to be
        computed only once. The next three options are slower because they
        recompute weights for each latitude.

        3: grid (x,y) in degrees, *width* in km, dx scaled by cosine(y),
        Cartesian distance calculation.

        4: grid (x,y) in degrees, *width* in km, Spherical distance
        calculation.

        5: grid (x,y) in Mercator ``projection='m1'`` img units, *width* in km,
        Spherical distance calculation.

    spacing : str
        ``xinc[+e|n][/yinc[+e|n]]``.
        x_inc [and optionally y_inc] is the grid spacing.
    nans : str or float
        ``i|p|r``.
        Determine how NaN-values in the input grid affects the filtered output.
    {R}
    toggle : bool
        Toggle the node registration for the output grid so as to become the
        opposite of the input grid. [Default gives the same registration as the
        input grid].
    {V}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the *outgrid* parameter is set:
        - xarray.DataArray if *outgrid* is not set
        - None if *outgrid* is set (grid output will be stored in *outgrid*)

    Examples
    --------
    >>> import os
    >>> import pygmt

    >>> # Apply a filter of 600km (full width) to the @earth_relief_30m file
    >>> # and return a filtered field (saved as netcdf)
    >>> pygmt.grdfilter(
    ...     grid="@earth_relief_30m",
    ...     filter="m600",
    ...     distance="4",
    ...     region=[150, 250, 10, 40],
    ...     spacing=0.5,
    ...     outgrid="filtered_pacific.nc",
    ... )
    >>> os.remove("filtered_pacific.nc")  # cleanup file

    >>> # Apply a gaussian smoothing filter of 600 km in the input data array,
    >>> # and returns a filtered data array with the smoothed field.
    >>> grid = pygmt.datasets.load_earth_relief()
    >>> smooth_field = pygmt.grdfilter(grid=grid, filter="g600", distance="4")
    """
    kind = data_kind(grid)

    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            if kind == "file":
                file_context = dummy_context(grid)
            elif kind == "grid":
                file_context = lib.virtualfile_from_grid(grid)
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(grid)))

            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdfilter", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            with xr.open_dataarray(outgrid) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        else:
            result = None  # if user sets an outgrid, return None

        return result


@fmt_docstring
@use_alias(
    A="transparency",
    C="cmap",
    D="background",
    F="color_model",
    G="truncate",
    H="output",
    I="reverse",
    L="limit",
    M="overrule_bg",
    N="no_bg",
    Q="log",
    R="region",
    T="series",
    V="verbose",
    W="categorical",
    Ww="cyclic",
    Z="continuous",
)
@kwargs_to_strings(T="sequence", G="sequence", L="sequence")
def grd2cpt(grid, **kwargs):
    """
    Make GMT color palette tables from a grid file.

    This is a module that will help you make static color palette tables
    (CPTs). By default, the CPT will simply be saved to the current session,
    but you can use *output* to save it to a file. You define an equidistant
    set of contour intervals or pass your own z-table or list, and create a new
    CPT based on an existing master (dynamic) CPT. The resulting CPT can be
    reversed relative to the master cpt, and can be made continuous or
    discrete. For color tables beyond the standard GMT offerings, visit
    `cpt-city <http://soliton.vm.bytemark.co.uk/pub/cpt-city/>`_ and
    `Scientific Colour-Maps <http://www.fabiocrameri.ch/colourmaps.php>`_.

    The CPT includes three additional colors beyond the range of z-values.
    These are the background color (B) assigned to values lower than the lowest
    *z*-value, the foreground color (F) assigned to values higher than the
    highest *z*-value, and the NaN color (N) painted wherever values are
    undefined.

    If the master CPT includes B, F, and N entries, these will be copied into
    the new master file. If not, the parameters :gmt-term:`COLOR_BACKGROUND`,
    :gmt-term:`COLOR_FOREGROUND`, and :gmt-term:`COLOR_NAN` from the
    :gmt-docs:`gmt.conf <gmt.conf>` file or the command line will be used. This
    default behavior can be overruled using the options *background*,
    *overrule_bg* or *no_bg*.

    The color model (RGB, HSV or CMYK) of the palette created by **grdcpt**
    will be the same as specified in the header of the master CPT. When there
    is no :gmt-term:`COLOR_MODEL` entry in the master CPT, the
    :gmt-term:`COLOR_MODEL` specified in the :gmt-docs:`gmt.conf <gmt.conf>`
    file or on the command line will be used.

    Full option list at :gmt-docs:`grd2cpt.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    transparency : str
        Sets a constant level of transparency (0-100) for all color slices.
        Append **+a** to also affect the fore-, back-, and nan-colors
        [Default is no transparency, i.e., 0 (opaque)].
    cmap : str
        Selects the master color palette table (CPT) to use in the
        interpolation. Full list of built-in color palette tables can be found
        at :gmt-docs:`cookbook/cpts.html#built-in-color-palette-tables-cpt`.
    background : bool or str
        Select the back- and foreground colors to match the colors for lowest
        and highest *z*-values in the output CPT [Default (``background=True``
        or ``background='o'``) uses the colors specified in the master file, or
        those defined by the parameters :gmt-term:`COLOR_BACKGROUND`,
        :gmt-term:`COLOR_FOREGROUND`, and :gmt-term:`COLOR_NAN`]. Use
        ``background='i'`` to match the colors for the lowest and highest
        values in the input (instead of the output) CPT.
    color_model :
        ``[R|r|h|c][+c[label]]``.
        Force output CPT to be written with r/g/b codes, gray-scale values or
        color name (**R**, default) or r/g/b codes only (**r**), or h-s-v codes
        (**h**), or c/m/y/k codes (**c**).  Optionally or alternatively, append
        **+c** to write discrete palettes in categorical format. If *label* is
        appended then we create labels for each category to be used when the
        CPT is plotted. The *label* may be a comma-separated list of category
        names (you can skip a category by not giving a name), or give
        *start*[-], where we automatically build monotonically increasing
        labels from *start* (a single letter or an integer). Append - to build
        ranges *start*-*start+1* instead.
    series : list or str
        ``[min/max/inc[+b|l|n]|file|list]``.
        Defines the range of the new CPT by giving the lowest and highest
        z-value (and optionally an interval). If this is not given, the
        existing range in the master CPT will be used intact. The values
        produced defines the color slice boundaries.  If **+n** is used it
        refers to the number of such boundaries and not the number of slices.
        For details on array creation, see
        :gmt-docs:`makecpt.html#generate-1d-array`.
    truncate : list or str
        ``zlo/zhi``.
        Truncate the incoming CPT so that the lowest and highest z-levels are
        to *zlo* and *zhi*. If one of these equal NaN then we leave that end of
        the CPT alone. The truncation takes place before any resampling. See
        also :gmt-docs:`cookbook/features.html#manipulating-cpts`.
    output : str
        Optional. The file name with extension .cpt to store the generated CPT
        file. If not given or False (default), saves the CPT as the session
        current CPT.
    reverse : str
        Set this to True or c [Default] to reverse the sense of color
        progression in the master CPT. Set this to z to reverse the sign of
        z-values in the color table. Note that this change of z-direction
        happens before *truncate* and *series* values are used so the latter
        must be compatible with the changed *z*-range. See also
        :gmt-docs:`cookbook/features.html#manipulating-cpts`.
    overrule_bg :
        Overrule background, foreground, and NaN colors specified in the master
        CPT with the values of the parameters :gmt-term:`COLOR_BACKGROUND`,
        :gmt-term:`COLOR_FOREGROUND`, and :gmt-term:`COLOR_NAN` specified in
        the :gmt-docs:`gmt.conf <gmt.conf>` file or on the command line. When
        combined with ``background``, only :gmt-term:`COLOR_NAN` is considered.
    no_bg : bool
        Do not write out the background, foreground, and NaN-color fields
        [Default will write them, i.e. ``no_bg=False``].
    log : bool
        For logarithmic interpolation scheme with input given as logarithms.
        Expects input z-values provided via ``series`` to be log10(*z*),
        assigns colors, and writes out *z*.
    continuous : bool
        Force a continuous CPT when building from a list of colors and a list
        of z-values [Default is None, i.e. discrete values].
    categorical : bool
        Do not interpolate the input color table but pick the output colors
        starting at the beginning of the color table, until colors for all
        intervals are assigned. This is particularly useful in combination with
        a categorical color table, like ``cmap='categorical'``.
    cyclic : bool
        Produce a wrapped (cyclic) color table that endlessly repeats its
        range. Note that ``cyclic=True`` cannot be set together with
        ``categorical=True``.
    {V}
    """
    kind = data_kind(grid)

    with GMTTempFile(suffix=".nc"):
        with Session() as lib:
            if kind == "file":
                file_context = dummy_context(grid)
            elif kind == "grid":
                file_context = lib.virtualfile_from_grid(grid)
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(grid)))

            with file_context as infile:
                if "W" in kwargs and "Ww" in kwargs:
                    raise GMTInvalidInput(
                        "Set only categorical or cyclic to True, not both."
                    )

                if "H" in kwargs.keys():  # if output file is set
                    outfile = kwargs.pop("H")
                    if not outfile or not isinstance(outfile, str):
                        raise GMTInvalidInput("'output' should be a proper file name.")
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grd2cpt", arg_str)
