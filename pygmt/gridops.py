"""
GMT modules for grid operations
"""

import xarray as xr


from .clib import Session
from .helpers import (
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    GMTTempFile,
    use_alias,
    data_kind,
    dummy_context,
)
from .exceptions import GMTInvalidInput


@fmt_docstring
@use_alias(
    G="outgrid",
    R="region",
    J="projection",
    N="extend",
    S="circ_subregion",
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
           G="outgrid",
           F="filter",
           D="distance"
           )
@kwargs_to_strings(R="sequence")

def grdfilter(grid, **kwargs):
    """
    filter a grid file in the time domain using one of the selected convolution
    or non-convolution isotropic or rectangular filters and compute distances
    using Cartesian or Spherical geometries. The output grid file can optionally
    be generated as a sub-region of the input (via *region*) and/or with new increment
    (via *spacing*) or registration (via *toggle*). In this way, one may have “extra space” in
    the input data so that the edges will not be used and the output can be within
    one half-width of the input edges. If the filter is low-pass, then the output
    may be less frequently sampled than the input.
        
    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
        outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {F} : str
        Name of filter type you which to apply, followed by the width
        b: Box Car; c: Cosine Arch; g: Gaussian; o: Operator; m: Median; p: Maximum Likelihood probability; h: histogram
        Example: 'm600' for a median filter with width of 600
    {D}: str
        Distance flag, that tells how grid (x,y) rrlated to the filter width as follows:
        flag = p: grid (px,py) with width an odd number of pixels; Cartesian distances.
        
        flag = 0: grid (x,y) same units as width, Cartesian distances.
        
        flag = 1: grid (x,y) in degrees, width in kilometers, Cartesian distances.
        
        flag = 2: grid (x,y) in degrees, width in km, dx scaled by cos(middle y), Cartesian distances.
        
        The above options are fastest because they allow weight matrix to be computed only once. The next three options are slower because they recompute weights for each latitude.
        
        flag = 3: grid (x,y) in degrees, width in km, dx scaled by cosine(y), Cartesian distance calculation.
        
        flag = 4: grid (x,y) in degrees, width in km, Spherical distance calculation.
        
        flag = 5: grid (x,y) in Mercator -Jm1 img units, width in km, Spherical distance calculation.
        
    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the *outgrid* parameter is set:
        - xarray.DataArray if *outgrid* is not set
        - None if *outgrid* is set (grid output will be stored in *outgrid*)
        
    Usage
    -------
    pygmt.grdfilter('/Users/Desktop/input.nc',F='m1600',D='4', G='/Users/Desktop/filtered_output.nc')
    Applies a filter of 1600km (full width) in the input.nc and returns a a filtered filed (saved as netcdf)
    
    out=pygmt.grdfiler(dataarray,F='g600',D='4')
    Applies a gaussian smoothing filter of 600 km in the input data array, and returns a filtered data array 
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
