"""
grdgradient - Create a gradient from a grid.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    A="azimuth",
    D="direction",
    E="radiance",
    G="outgrid",
    R="region",
    V="verbose",
)
@kwargs_to_strings(
    A="sequence", R="sequence",
)
def grdgradient(grid, **kwargs):
    r"""
    Full option list at :gmt-docs:`grdgradient.html`

    {aliases}
    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    azimuth : str or list or xarray.DataArray
        *azim*\ [/*azim2*].
        Azimuthal direction for a directional derivative; *azim* is the
        angle in the x,y plane measured in degrees positive clockwise from
        north (the +y direction) toward east (the +x direction). The
        negative of the directional derivative, -[dz/dx\*sin(*azim*) +
        dz/dy\*cos(\ *azim*)], is found; negation yields positive values
        when the slope of z(x,y) is downhill in the *azim* direction, the
        correct sense for shading the illumination of an image by a light
        source above the x,y plane shining from the *azim* direction.
        Optionally, supply two azimuths, *azim*/*azim2*, in which case the
        gradients in each of these directions are calculated and the one
        larger in magnitude is retained; this is useful for illuminating data
        with two directions of lineated structures, e.g., *0*/*270*
        illuminates from the north (top) and west (left).  Finally, if *azim*
        is a file it must be a grid of the same domain, spacing and
        registration as *ingrid* that will update the azimuth at each output
        node when computing the directional derivatives.
    {R}
    {V}
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdgradient", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            with xr.open_dataarray(outgrid) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        else:
            result = None  # if user sets an outgrid, return None

        return result
