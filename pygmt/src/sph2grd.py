"""
sph2grd - Compute grid from spherical harmonic coefficients
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["sph2grd"]


@fmt_docstring
@use_alias(
    I="spacing",
    R="region",
    V="verbose",
    b="binary",
    h="header",
    i="incols",
    r="registration",
    x="cores",
)
@kwargs_to_strings(I="sequence", R="sequence", i="sequence_comma")
def sph2grd(data, outgrid: str | None = None, **kwargs) -> xr.DataArray | None:
    r"""
    Create spherical grid files in tension of data.

    Reads a spherical harmonics coefficient table with records of L, M,
    C[L,M], S[L,M] and evaluates the spherical harmonic model on the
    specified grid.

    Full option list at :gmt-docs:`sph2grd.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        Pass in data with L, M, C[L,M], S[L,M] values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    {outgrid}
    {spacing}
    {region}
    {verbose}
    {binary}
    {header}
    {incols}
    {registration}
    {cores}

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Create a new grid from the remote file "EGM96_to_36.txt",
    >>> # set the grid spacing to 1 arc-degree, and the region to global ("g")
    >>> new_grid = pygmt.sph2grd(data="@EGM96_to_36.txt", spacing=1, region="g")
    """
    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="vector", data=data) as vintbl,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(
                module="sph2grd", args=build_arg_list(kwargs, infile=vintbl)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
