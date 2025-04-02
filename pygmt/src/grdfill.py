"""
grdfill - Interpolate across holes in a grid.
"""

import warnings

import numpy as np
import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    deprecate_parameter,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)

__doctest_skip__ = ["grdfill"]


def _validate_params(
    constantfill=None,
    gridfill=None,
    neighborfill=None,
    splinefill=None,
    inquire=False,
    mode=None,
):
    """
    Validate the fill/inquire parameters.

    >>> _validate_params(constantfill=20.0)
    >>> _validate_params(inquire=True)
    >>> _validate_params(mode="c20.0")
    >>> _validate_params(constantfill=20.0, gridfill="bggrid.nc")
    Traceback (most recent call last):
    ...
    pygmt.exceptions.GMTInvalidInput: Parameters ... are mutually exclusive.
    >>> _validate_params(constantfill=20.0, inquire=True)
    Traceback (most recent call last):
    ...
    pygmt.exceptions.GMTInvalidInput: Parameters ... are mutually exclusive.
    >>> _validate_params()
    Traceback (most recent call last):
    ...
    pygmt.exceptions.GMTInvalidInput: Need to specify parameter ...
    """
    _fill_params = "'constantfill'/'gridfill'/'neighborfill'/'splinefill'"
    # The deprecated 'mode' parameter is given.
    if mode is not None:
        msg = (
            "The 'mode' parameter is deprecated since v0.15.0 and will be removed in "
            f"v0.19.0. Use {_fill_params} instead."
        )
        warnings.warn(msg, FutureWarning, stacklevel=2)

    n_given = sum(
        param is not None and param is not False
        for param in [constantfill, gridfill, neighborfill, splinefill, inquire, mode]
    )
    if n_given > 1:  # More than one mutually exclusive parameter is given.
        msg = f"Parameters {_fill_params}/'inquire'/'mode' are mutually exclusive."
        raise GMTInvalidInput(msg)
    if n_given == 0:  # No parameters are given.
        msg = (
            f"Need to specify parameter {_fill_params} for filling holes or "
            "'inquire' for inquiring the bounds of each hole."
        )
        raise GMTInvalidInput(msg)


def _parse_fill_mode(
    constantfill=None, gridfill=None, neighborfill=None, splinefill=None
) -> str | None:
    """
    Parse the fill parameters and return the appropriate string for the -A option.

    >>> import numpy as np
    >>> import xarray as xr
    >>> _parse_fill_mode(constantfill=20.0)
    'c20.0'
    >>> _parse_fill_mode(gridfill="bggrid.nc")
    'g'
    >>> _parse_fill_mode(gridfill=xr.DataArray(np.zeros((10, 10))))
    'g'
    >>> _parse_fill_mode(neighborfill=20)
    'n20'
    >>> _parse_fill_mode(neighborfill=True)
    'n'
    >>> _parse_fill_mode(splinefill=0.5)
    's0.5'
    >>> _parse_fill_mode(splinefill=True)
    's'
    """
    if constantfill is not None:
        return f"c{constantfill}"
    if gridfill is not None:
        return "g"  # Append grid file name later to support xarray.DataArray.
    if neighborfill is not None and neighborfill is not False:
        return "n" if neighborfill is True else f"n{neighborfill}"
    if splinefill is not None and splinefill is not False:
        return "s" if splinefill is True else f"s{splinefill}"
    return None


@fmt_docstring
# TODO(PyGMT>=0.19.0): Remove the deprecated 'no_data' parameter.
# TODO(PyGMT>=0.19.0): Remove the deprecated 'mode' parameter.
@deprecate_parameter("no_data", "hole", "v0.15.0", remove_version="v0.19.0")
@use_alias(N="hole", R="region", V="verbose", f="coltypes")
@kwargs_to_strings(R="sequence")
def grdfill(
    grid: str | xr.DataArray,
    outgrid: str | None = None,
    constantfill: float | None = None,
    gridfill: str | xr.DataArray | None = None,
    neighborfill: float | bool | None = None,
    splinefill: float | bool | None = None,
    inquire: bool = False,
    mode: str | None = None,
    **kwargs,
) -> xr.DataArray | np.ndarray | None:
    r"""
    Interpolate across holes in a grid.

    Read a grid that presumably has unfilled holes that the user wants to fill in some
    fashion. Holes are identified by NaN values but this criteria can be changed via the
    ``hole`` parameter. There are several different algorithms that can be used to
    replace the hole values. If no holes are found the original unchanged grid is
    returned.

    Full option list at :gmt-docs:`grdfill.html`.

    {aliases}

    Parameters
    ----------
    {grid}
    {outgrid}
    constantfill
        Fill the holes with a constant value. Specify the constant value to use.
    gridfill
        Fill the holes with values sampled from another (possibly coarser) grid. Specify
        the grid (a file name or an :class:`xarray.DataArray`) to use for the fill.
    neighborfill
        Fill the holes with the nearest neighbor. Specify the search radius in pixels.
        If set to ``True``, the default search radius will be used
        (:math:`r^2 = \sqrt{{n^2 + m^2}}`, where (*n,m*) are the node dimensions of the
        grid).
    splinefill
        Fill the holes with a bicubic spline. Specify the tension value to use. If set
        to ``True``, no tension will be used.
    hole : float
        Set the node value used to identify a point as a member of a hole [Default is
        NaN].
    inquire
        Output the bounds of each hole. The bounds are returned as a 2-D numpy array in
        the form of (west, east, south, north). No grid fill takes place and ``outgrid``
        is ignored.
    mode
        Specify the hole-filling algorithm to use. Choose from **c** for constant fill
        and append the constant value, **n** for nearest neighbor (and optionally append
        a search radius in pixels [default radius is :math:`r^2 = \sqrt{{ X^2 + Y^2 }}`,
        where (*X,Y*) are the node dimensions of the grid]), or **s** for bicubic spline
        (optionally append a *tension* parameter [Default is no tension]).

        .. deprecated:: 0.15.0
            Use ``constantfill``, ``gridfill``, ``neighborfill``, or ``splinefill``
            instead. The parameter will be removed in v0.19.0.
    {region}
    {coltypes}
    {verbose}

    Returns
    -------
    ret
        If ``inquire`` is ``True``, return the bounds of each hole as a 2-D numpy array.
        Otherwise, the return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - ``None`` if ``outgrid`` is set (grid output will be stored in the file set by
          ``outgrid``)

    Example
    -------
    Fill holes in a bathymetric grid with a constant value of 20.
    >>> import pygmt
    >>> # Load a bathymetric grid with missing data
    >>> earth_relief_holes = pygmt.datasets.load_sample_data(name="earth_relief_holes")
    >>> # Fill the holes with a constant value of 20
    >>> filled_grid = pygmt.grdfill(grid=earth_relief_holes, constantfill=20)

    Inquire the bounds of each hole.
    >>> pygmt.grdfill(grid=earth_relief_holes, inquire=True)
    array([[1.83333333, 6.16666667, 3.83333333, 8.16666667],
           [6.16666667, 7.83333333, 0.5       , 2.5       ]])
    """
    # Validate the fill/inquire parameters.
    _validate_params(constantfill, gridfill, neighborfill, splinefill, inquire, mode)

    # Parse the fill parameters and return the appropriate string for the -A option.
    kwargs["A"] = (
        _parse_fill_mode(constantfill, gridfill, neighborfill, splinefill)
        if mode is None
        else mode
    )

    with Session() as lib:
        with lib.virtualfile_in(check_kind="raster", data=grid) as vingrd:
            if inquire:  # Inquire mode.
                kwargs["L"] = True
                with lib.virtualfile_out(kind="dataset") as vouttbl:
                    lib.call_module(
                        module="grdfill",
                        args=build_arg_list(kwargs, infile=vingrd, outfile=vouttbl),
                    )
                    return lib.virtualfile_to_dataset(
                        vfname=vouttbl, output_type="numpy"
                    )

            # Fill mode.
            with (
                lib.virtualfile_in(
                    check_kind="raster", data=gridfill, required_data=False
                ) as vbggrd,
                lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
            ):
                if gridfill is not None:
                    # Fill by a grid. Append the actual or virtual grid file name.
                    kwargs["A"] = f"g{vbggrd}"
                kwargs["G"] = voutgrd
                lib.call_module(
                    module="grdfill", args=build_arg_list(kwargs, infile=vingrd)
                )
                return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
