"""
grdproject - Forward and inverse map transformation of grids.
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
    C="center",
    D="spacing",
    E="dpi",
    F="scaling",
    G="outgrid",
    J="projection",
    I="inverse",
    M="unit",
    R="region",
    V="verbose",
    n="interpolation",
    r="registration",
)
@kwargs_to_strings(C="sequence", R="sequence")
def grdproject(grid, **kwargs):
    r"""
    Change projection of gridded data between geographical and rectangular.

    This module will project a geographical gridded data set onto a
    rectangular grid. If ``inverse`` is ``True``, it will project a
    rectangular coordinate system to a geographic system. To obtain the value
    at each new node, its location is inversely projected back onto the input
    grid after which a value is interpolated between the surrounding input
    grid values. By default bi-cubic interpolation is used. Aliasing is
    avoided by also forward projecting the input grid nodes. If two or more
    nodes are projected onto the same new node, their average will dominate in
    the calculation of the new node value. Interpolation and aliasing is
    controlled with the ``interpolation`` option. The new node spacing may be
    determined in one of several ways by specifying the grid spacing, number
    of nodes, or resolution. Nodes not constrained by input data are set to
    NaN. The ``region`` parameter can be used to select a map region larger or
    smaller than that implied by the extent of the grid file.

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    inverse : bool
        When set to ``True`` transforms grid from rectangular to
        geographical [Default is False].
    {J}
    {R}
    center : str or list
        [*dx*, *dy*].
        Let projected coordinates be relative to projection center [Default
        is relative to lower left corner]. Optionally, add offsets in the
        projected units to be added (or subtracted when ``inverse`` is set) to
        (from) the projected coordinates, such as false eastings and
        northings for particular projection zones [0/0].
    {I}
    dpi : int
        Set the resolution for the new grid in dots per inch.
    scaling : str
        [**c**\|\ **i**\|\ **p**\|\ **e**\|\ **f**\|\
        **k**\|\ **M**\|\ **n**\|\ **u**].
        Force 1:1 scaling, i.e., output or output data are in actual projected
        meters [**e**]. To specify other units, append **f** (foot),
        **k** (km), **M** (statute mile), **n** (nautical mile), **u**
        (US survey foot), **i** (inch), **c** (cm), or **p** (point).
    unit : str
        Append **c**, **i**, or **p** to indicate that cm, inch, or point
        should be the projected measure unit. Cannot be used with ``scaling``.
    {V}
    {n}
    {r}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    if "J" not in kwargs.keys():
        raise GMTInvalidInput("The projection must be specified.")
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdproject", arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
