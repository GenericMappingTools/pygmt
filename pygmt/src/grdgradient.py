"""
grdgradient - Compute directional gradients from a grid.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    args_in_kwargs,
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
    n="interpolation",
)
@kwargs_to_strings(A="sequence", E="sequence", R="sequence")
def grdgradient(grid, **kwargs):
    r"""
    Compute the directional derivative of the vector gradient of the data.

    Can accept ``azimuth``, ``direction``, and ``radiance`` input to create
    the resulting gradient.

    Full option list at :gmt-docs:`grdgradient.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    azimuth : int or float or str or list
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
        registration as *grid* that will update the azimuth at each output
        node when computing the directional derivatives.
    direction : str
        [**a**][**c**][**o**][**n**].
        Find the direction of the positive (up-slope) gradient of the data.
        To instead find the aspect (the down-slope direction), use **a**.
        By default, directions are measured clockwise from north, as *azim*
        in ``azimuth``. Append **c** to use conventional Cartesian angles
        measured counterclockwise from the positive x (east) direction.
        Append **o** to report orientations (0-180) rather than
        directions (0-360). Append **n** to add 90 degrees to all angles
        (e.g., to give local strikes of the surface).
    radiance : str or list
        [**m**\|\ **s**\|\ **p**]\ *azim/elev*\ [**+a**\ *ambient*][**+d**\
        *diffuse*][**+p**\ *specular*][**+s**\ *shine*].
        Compute Lambertian radiance appropriate to use with ``grdimage``
        and ``grdview``. The Lambertian Reflection assumes an ideal surface
        that reflects all the light that strikes it and the surface appears
        equally bright from all viewing directions. Here, *azim* and *elev* are
        the azimuth and elevation of the light vector. Optionally, supply
        *ambient* [0.55], *diffuse* [0.6], *specular* [0.4], or *shine* [10],
        which are parameters that control the reflectance properties of the
        surface. Default values are given in the brackets. Use **s** for a
        simpler Lambertian algorithm. Note that with this form you only have
        to provide azimuth and elevation. Alternatively, use **p** for
        the Peucker piecewise linear approximation (simpler but faster
        algorithm; in this case the *azim* and *elev* are hardwired to 315
        and 45 degrees. This means that even if you provide other values
        they will be ignored.)
    {R}
    {V}
    {n}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        if not args_in_kwargs(args=["A", "D", "E"], kwargs=kwargs):
            raise GMTInvalidInput(
                """At least one of the following parameters must be specified:
                azimuth, direction, or radiance"""
            )
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
